package dataloader; 

import (
	"net/http" 
	"bytes" 
	"encoding/json"
	"io" 
	"fmt" 
)

func AccessPageCount(url string, ch chan PageCountResponseCh, baseRequestJson BaseRequestModel)  {
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
		url + "/pdf_page_count", 
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

	
