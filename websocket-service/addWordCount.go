package main 

import (
	"net/http"
	"encoding/json" 
	"bytes" 
	"fmt" 
) 

type AddWordCountRequestModel struct {
	FileName 	string 	`json:"filename"`
	EmailId		string 	`json:"email_id"`
} 

func (pm *ProcessMetadata) AddWordCount(url string) error {
	client := &http.Client{}; 
	wordCountJson := AddWordCountRequestModel {
		FileName: 	pm.FileName, 
		EmailId : 	pm.EmailId, 
	};  

	wordCountBuf, err := json.Marshal(wordCountJson); 
	if err != nil {
		return err
	} 

	reader := bytes.NewReader(wordCountBuf); 
	request, err := http.NewRequest(
		http.MethodPost, 
		url + "/add_word_count", 
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
		return fmt.Errorf("error : %s -> Add word count", err.Error()); 
	} 

	return nil 

} 
