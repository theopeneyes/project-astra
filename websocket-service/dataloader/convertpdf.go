package dataloader; 

import (
	"encoding/json"
	"net/http"
	"bytes"
	"log" 
	
) 

func RunPdfConverter(url string, errChannel chan error, baseRequestJson BaseRequestModel) {
	client := &http.Client{}; 
	convertRequestBody, err := json.Marshal(baseRequestJson); 
	log.Println("Request Body:", string(convertRequestBody)); 
	if err != nil {
		log.Println("Error occured after marshalling"); 
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
		log.Println("Error occured after request making"); 
		errChannel <- err; 
		return 
	} 

	convertPdfRequest.Header.Add("Content-Type", "application/json"); 

	res, err := client.Do(convertPdfRequest); 
	if err != nil {
		log.Printf("Error occured after client request making: %+v\n", convertPdfRequest); 
		errChannel <- err 
		return 
	} 
	
	if res.StatusCode != http.StatusOK {
		log.Println("Status code error"); 
		errChannel <- err; 
		return 
	} 
	
	errChannel <- nil; 
	return 
} 
