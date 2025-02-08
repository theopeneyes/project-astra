package main 

import (
	"net/http" 
	"encoding/json"
	"io" 
	"bytes" 
	"fmt" 
	"log" 
) 

type BaseRequestModel struct {
	FileName 	string `json:"filename"`
	EmailId 	string `json:"email_id"`
} 

type PageCountResponseModel struct {
	FileName 	string `json:"filename"`
	EmailId 	string `json:"email_id"` 
	Time 		float32 `json:"time"`
	PageCount	int32 `json:"page_count"`
} 

type PageCountResponseCh struct {
	Error 		error 
	PageCount 	int32
} 

type LanguageResponseModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	TokenCount 	int32 	`json:"token_count"`
	Time 		float32 `json:"time"`
	LanguageCode 	string `json:"detected_language"`
	Confidence 	float32 `json:"confidence"`
}

type ExtractContentsPageRequestModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	LanguageCode 	string 	`json:"language_code"`
	PageNumbers 	int32 	`json:"number_of_pages"`
} 

type ExtractContentsPageResponseModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	TokenCount 	int32 	`json:"token_count"`
	Time 		float32 `json:"time"`
	FirstPage 	int32 	`json:"first_page"`
	LastPage 	int32 	`json:"last_page"`
} 

type ChapterPageRequestModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	FirstPage 	int32 	`json:"first_page"`
	LastPage 	int32 	`json:"last_page"`
	LanguageCode 	string 	`json:"language_code"`
} 

type ChapterPageResponseModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	Time 		float32 `json:"time"`
	TokenCount 	int32 	`json:"token_count"`
} 

func runChapterWiseSegmentation(request ExtractContentsPageRequestModel) error {
	client := &http.Client{}; 
	requestBody, err := json.Marshal(request); 
	if err != nil {
		return err; 
	} 
	
	requestReader := bytes.NewReader(requestBody);  
	
	requestExtractContentsPage, err := http.NewRequest(
		http.MethodPost, 
		LlmServerURL + "/extract_contents_page", 
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
		LlmServerURL + "/identify/chapter_pages", 
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
		LlmServerURL + "/reform/chapter_pages", 
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

func runPdfConverter(errChannel chan error, baseRequestJson BaseRequestModel) {
	client := &http.Client{}; 
	convertRequestBody, err := json.Marshal(baseRequestJson); 
	if err != nil {
		errChannel <- err; 
		return
	} 

	reader := bytes.NewReader(convertRequestBody); 
	
	convertPdfRequest, err := http.NewRequest(
		http.MethodPost, 
		LlmServerURL + "/convert_pdf", 
		reader, 
	); 
	
	if err != nil {
		errChannel <- err; 
		return 
	} 

	convertPdfRequest.Header.Add("Content-Type", "application/json"); 

	res, err := client.Do(convertPdfRequest); 
	if res.StatusCode != http.StatusOK {
		errChannel <- err; 
		return 
	} 
	
	errChannel <- nil; 
	return 

} 

func accessPageCount(ch chan PageCountResponseCh, baseRequestJson BaseRequestModel)  {
	client := &http.Client{}; 
	pageCountRequestBody, err := json.Marshal(baseRequestJson); 
	if err != nil {
		ch <- PageCountResponseCh {
			Error: err, 
			PageCount: 0, 
		} 
		return 	
	} 

	reader := bytes.NewReader(pageCountRequestBody); 

	pageCountRequest, err := http.NewRequest(
		http.MethodPost, 
		LlmServerURL + "/pdf_page_count", 
		reader, 
	); 
	
	if err != nil {
		ch <- PageCountResponseCh {
			Error: err, 
			PageCount: 0, 
		} 
	} 
	
	pageCountRequest.Header.Add("Content-Type", "application/json"); 
	res, err := client.Do(pageCountRequest); 
	if err != nil {
		ch <- PageCountResponseCh {
			Error: err, 
			PageCount: 0, 
		} 
		return 	
	} 

	if res.StatusCode != http.StatusOK {
		ch <- PageCountResponseCh {
			Error: fmt.Errorf("%s", http.StatusText(res.StatusCode)), 
			PageCount: 0,  
		} 
	} 
	
	respBytes, err := io.ReadAll(res.Body);  
	if err != nil {
		
		ch <- PageCountResponseCh {
			Error: err, 
			PageCount: 0, 
		} 
		return 	
	} 
	
	pageCountResponseBody := PageCountResponseModel{}; 
	json.Unmarshal( respBytes, &pageCountResponseBody); 

	ch <- PageCountResponseCh{
		Error: nil, 
		PageCount: pageCountResponseBody.PageCount,  
	}; 
	
	return 

} 

func detectLanguage(baseRequestJson BaseRequestModel) (string, error) {
	client := &http.Client{}; 
	langRequestBody, err := json.Marshal(baseRequestJson);  
	if err != nil {
		return "", err; 
	} 
	
	langReader := bytes.NewReader(langRequestBody); 
	langRequest, err := http.NewRequest(
		http.MethodPost, 
		LlmServerURL + "/detect_lang", 
		langReader, 
	); 
	
	if err != nil {
		return "", err;  
	} 
	
	resp, err := client.Do(langRequest); 
	if err != nil {
		return "",  err;  
	} 
	
	if resp.StatusCode != http.StatusOK {
		return "",  err;  
	} 

	responseJsonBody, err := io.ReadAll(resp.Body); 
	if err != nil {
		return "", err; 
	} 
	
	responseJson := LanguageResponseModel{};  
	err = json.Unmarshal(responseJsonBody, &responseJson); 
	if err != nil {
		return "", err;  
	} 
	
	return responseJson.LanguageCode, err; 
	
} 

func (pm *ProcessMetadata) DataLoader() error {
	baseRequestJson := BaseRequestModel {
		FileName: pm.FileName, 
		EmailId: pm.EmailId, 
	};  

	log.Println("Initiated process of converting pdf and getting pages.."); 

	pageCh := make(chan PageCountResponseCh); 
	errCh := make (chan error); 
	go runPdfConverter(errCh, baseRequestJson);  
	go accessPageCount(pageCh, baseRequestJson);  

	err := <- errCh; 
	pageResponse := <- pageCh; 

	if err != nil {
		return err; 
	} 
	
	if pageResponse.Error != nil {
		return pageResponse.Error; 
	} 
	
	if pageResponse.PageCount > 20 {
		pageResponse.PageCount = 20; 
	} 

	log.Println("Converting and page count getting complete."); 
	log.Println("Getting Language codes..."); 

	languageCode, err := detectLanguage(baseRequestJson); 
	if err != nil {
		return err; 
	} 

	fmt.Printf("The language code : %s\n", languageCode); 
	log.Println("Language codes accessed!"); 
	
	log.Println("Running chapter wise segmentation..."); 
	
	extractContentsPageJson := ExtractContentsPageRequestModel{
		FileName: pm.FileName, 
		EmailId: pm.EmailId, 
		PageNumbers: pageResponse.PageCount,  
		LanguageCode: languageCode, 
	} 
	
	err = runChapterWiseSegmentation(extractContentsPageJson); 
	if err != nil {
		return nil; 
	} 
	return nil; 
} 
	


