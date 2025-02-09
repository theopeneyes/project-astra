package dataloader; 

import (
	"encoding/json"
	"net/http"
	"bytes"
	
) 

func RunPdfConverter(url string, errChannel chan error, baseRequestJson BaseRequestModel) {
	client := &http.Client{}; 
	convertRequestBody, err := json.Marshal(baseRequestJson); 
	if err != nil {
		errChannel <- err; 
		return
	} 

	reader := bytes.NewReader(convertRequestBody); 
	
	convertPdfRequest, err := http.NewRequest(
		http.MethodPost, 
		url + "/convert_pdf", 
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
