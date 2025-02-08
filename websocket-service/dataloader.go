package main 

import (
	"net/http" 
	"encoding/json"
	"io" 
	"bytes" 
	"fmt" 
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

type PageCountResponseChannel struct {
	Error error 
	PageCount int32
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

func accessPageCount(ch chan PageCountResponseChannel, baseRequestJson BaseRequestModel)  {
	client := &http.Client{}; 
	pageCountRequestBody, err := json.Marshal(baseRequestJson); 
	if err != nil {
		ch <- PageCountResponseChannel {
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
		ch <- PageCountResponseChannel {
			Error: err, 
			PageCount: 0, 
		} 
	} 
	
	pageCountRequest.Header.Add("Content-Type", "application/json"); 
	res, err := client.Do(pageCountRequest); 
	if err != nil {
		ch <- PageCountResponseChannel {
			Error: err, 
			PageCount: 0, 
		} 
		return 	
	} 
	
	respBytes, err := io.ReadAll(res.Body);  
	if err != nil {
		
		ch <- PageCountResponseChannel {
			Error: err, 
			PageCount: 0, 
		} 
		return 	
	} 
	
	pageCountResponseBody := PageCountResponseModel{}; 
	json.Unmarshal( respBytes, &pageCountResponseBody); 

	ch <- PageCountResponseChannel{
		Error: nil, 
		PageCount: pageCountResponseBody.PageCount,  
	}; 
	
	return 

} 

func (pm *ProcessMetadata) DataLoader() error {
	baseRequestJson := BaseRequestModel {
		FileName: pm.FileName, 
		EmailId: pm.EmailId, 
	};  

	pageCh := make(chan PageCountResponseChannel); 
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
	
	fmt.Printf("Successfully retrieved page numbers: %+v\n", pageResponse); 
	return nil; 
} 
	


