package dataloader; 

import (
	"net/http"
	"bytes" 
	"encoding/json" 
	"io"
)

func DetectLanguage(url string, baseRequestJson BaseRequestModel) (string, error) {
	client := &http.Client{}; 
	langRequestBody, err := json.Marshal(baseRequestJson);  
	if err != nil {
		return "", err; 
	} 
	
	langReader := bytes.NewReader(langRequestBody); 
	langRequest, err := http.NewRequest(
		http.MethodPost, 
		url + "/detect_lang", 
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

