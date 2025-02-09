package dataloader; 

import (
	"encoding/json" 
	"io"
	"net/http"
	"fmt" 
	"bytes"
) 

func RunChapterWiseSegmentation(url string, request ExtractContentsPageRequestModel) error {
	client := &http.Client{}; 
	requestBody, err := json.Marshal(request); 
	if err != nil {
		return err; 
	} 
	
	requestReader := bytes.NewReader(requestBody);  
	
	requestExtractContentsPage, err := http.NewRequest(
		http.MethodPost, 
		url + "/extract_contents_page", 
		requestReader, 
	); 
	
	if err != nil {
		return err; 
	} 
	
	res, err := client.Do(requestExtractContentsPage); 
	if err != nil {
		return err; 
	} 
	
	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("%s", http.StatusText(res.StatusCode)); 
	} 
	
	resBuff, err := io.ReadAll(res.Body); 
	if err != nil {
		return err; 
	} 
	
	contentsPageResponse := ExtractContentsPageResponseModel{}; 
	err = json.Unmarshal(resBuff, &contentsPageResponse); 
	if err != nil {
		return err; 
	} 
	
	identifyJson := ChapterPageRequestModel {
		FileName: request.FileName, 
		EmailId: request.EmailId, 
		FirstPage: contentsPageResponse.FirstPage, 
		LastPage: contentsPageResponse.LastPage, 
		LanguageCode: request.LanguageCode, 
	}  
	
	identifyJsonBody, err := json.Marshal(identifyJson); 
	if err != nil {
		return err; 
	}  
	
	identifyReader := bytes.NewReader(identifyJsonBody); 
	requestIdentifyChapterPages, err := http.NewRequest(
		http.MethodPost,
		url + "/identify/chapter_pages", 
		identifyReader, 
	); 
	
	if err != nil {	
		return err;  
	} 
	
	res, err = client.Do(requestIdentifyChapterPages); 
	if err != nil {
		return err; 
	} 
	
	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("%s", http.StatusText(res.StatusCode)); 
	} 
	
	resReader, err := io.ReadAll(res.Body); 
	chapterPageResponse := ChapterPageResponseModel{}; 
	
	err = json.Unmarshal(resReader, &chapterPageResponse); 
	if err != nil {
		return err; 
	} 
	
	baseRequestJson := BaseRequestModel {
		FileName: chapterPageResponse.FileName, 
		EmailId: chapterPageResponse.EmailId, 
	} 

	baseRequestBody, err := json.Marshal(baseRequestJson); 
	if err != nil {
		return err; 
	} 

	baseReqReader := bytes.NewReader(baseRequestBody); 
	
	reformRequest, err := http.NewRequest(
		http.MethodPost, 
		url + "/reform/chapter_pages", 
		baseReqReader, 
	); 

	if err != nil {
		return err; 
	} 
	
	res, err = client.Do(reformRequest);  
	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("%s", http.StatusText(res.StatusCode)); 
	} 
	
	return nil;  
} 
