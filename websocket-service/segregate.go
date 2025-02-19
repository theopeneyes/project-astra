package main 

import (
	"net/http" 
	"encoding/json" 
	"bytes" 
	"io" 
	"fmt" 
) 

type SegregateRequestModel struct {
	FileName 	string	`json:"filename"`  
	EmailId 	string	`json:"email_id"` 
} 

type SegregateResponseModel struct {
	FileName 	string 		`json:"filename"`
	EmailId 	string 		`json:"email_id"`
	TokenCount 	int 		`json"token_count"`
	Time 		float32 	`json:"time"`	
} 

func (pm *ProcessMetadata) Segregate(url string) error {
	client := &http.Client{};  
	segregateJson := SegregateRequestModel {
		EmailId: 	pm.EmailId, 
		FileName: 	pm.FileName, 
	} 

	dataBuf, err := json.Marshal(segregateJson); 
	if err != nil {
		return err 
	} 

	reader := bytes.NewReader(dataBuf); 
	request, err  := http.NewRequest(
		http.MethodPost, 
		url + "/segregate", 
		reader, 
	);  

	if err != nil {
		return err 
	} 

	res, err := client.Do(request); 
	if err != nil {
		return err 
	}

	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("error: %s -> Segregation error", err.Error()); 
	}

	resBuf, err := io.ReadAll(res.Body); 
	if err != nil {
		return err 
	} 

	responseJson := SegregateResponseModel {};  
	err = json.Unmarshal(resBuf, &responseJson); 
	if err != nil {
		return err 
	} 

	return nil ; 
} 
