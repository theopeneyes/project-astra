package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

type QnaGenerationModel struct {
	EmailId string `json:"email_id"`
	FileName string `json:"filename"`
} 

func (pm *ProcessMetadata) GenerateQNA(url string) error {
	client := http.Client{} 
	payload := QnaGenerationModel {
		EmailId: pm.EmailId,
		FileName: pm.FileName,
	} 

	buf, err := json.Marshal(payload) 
	if err != nil {
		return err 
	} 

	readBuf := bytes.NewReader(buf)
	request, err := http.NewRequest(
		http.MethodPost, 
		LlmServerURL + "/generate_excel", 
		readBuf, 
	)

	if err != nil {
		return err 
	} 

	res, err := client.Do(request)
	if err != nil {
		return err 
	}
	
	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("error occured while sending this request"); 
	} 

	return nil 

}
