package main 

import (
	"net/http" 
	"encoding/json" 
	"bytes" 
	"io" 
	"fmt" 
) 

type PreprocessRequestModel struct {
	FileName 	string `json:"filename"`
	EmailId		string `json:"email_id"`
} 

type PreprocessResponseModel struct {
	FileName 	string 	`json:"filename"`
	EmailId		string 	`json:"email_id"`
	Time 		float32 `json:"time"`
} 


func (pm *ProcessMetadata) Preprocess(url string) error {
	client := &http.Client{}; 
	preprocessedJson := PreprocessRequestModel {
		FileName: 	pm.FileName, 
		EmailId	: 	pm.EmailId, 
	};  

	dataBuf, err := json.Marshal(preprocessedJson)
	if err != nil {
		return err; 
	} 

	dataReader := bytes.NewReader(dataBuf); 
	request, err := http.NewRequest(
		http.MethodPost, 
		url + "/preprocess_for_graph", 
		dataReader, 
	); 

	if err != nil {
		return err;  
	} 

	res, err := client.Do(request); 
	if err != nil {
		return err; 
	}
	
	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("error: %s -> Preprocess error", 
		http.StatusText(res.StatusCode)); 
	} 

	resBuf, err := io.ReadAll(res.Body); 
	preprocessResponse := PreprocessResponseModel {} 
	err = json.Unmarshal(resBuf, &preprocessResponse); 
	if err != nil {
		return err 
	} 

	return nil 
} 
