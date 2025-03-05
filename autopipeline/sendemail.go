package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

type EmailRequest struct {
	EmailId string `json:"email"`
} 

func (pm *ProcessMetadata) SendEmailToClient(url string) error {
	buf, err := json.Marshal(EmailRequest{
		EmailId: pm.EmailId,
	})

	if err != nil {
		return err
	} 

	reqBody := bytes.NewReader(buf); 
	request, err := http.NewRequest(http.MethodPost, url + "/send-email", reqBody); 
	if err != nil {
		return err
	} 

	client := http.Client{} 
	res, err := client.Do(request); 
	if err != nil {
		return err 
	}
	
	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("error occured while sending email"); 
	} 

	return nil 
}