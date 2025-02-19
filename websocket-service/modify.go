package main 

import (
	"sync" 
	"net/http" 
	"fmt" 
	"encoding/json" 
	"bytes" 
) 

type ErrorNode struct {
	Err 		error 
	Request 	*http.Request
} 

type ErrorChan struct {
	mu 		sync.Mutex 
	Errors 		[] ErrorNode  
} 

func (ec *ErrorChan) AddErrorNode(err ErrorNode) {
	ec.mu.Lock(); 
	defer ec.mu.Unlock(); 
	ec.Errors = append(ec.Errors, err); 
} 

type ModifyRequestModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`	
	BranchName 	string 	`json:"branch_name"`
} 

func (pm *ProcessMetadata) Modify( url string ) ErrorChan {
	var errChan ErrorChan; 
	client := &http.Client{}; 
	topicJson := ModifyRequestModel {
		FileName  : 	pm.FileName, 
		EmailId   : 	pm.EmailId, 
		BranchName: 	"topic",  
	} 


	conceptJson := ModifyRequestModel {
		FileName  : 	pm.FileName, 
		EmailId   : 	pm.EmailId, 
		BranchName: 	"concept",  
	} 

	headingJson := ModifyRequestModel {
		FileName  : 	pm.FileName, 
		EmailId   : 	pm.EmailId, 
		BranchName: 	"heading_text",  
	} 

	topicBuf, err := json.Marshal(topicJson); 
	if err != nil {
		errChan.Errors = append(errChan.Errors, ErrorNode {
			Err: err, 
			Request: nil, 
		})

		return errChan   
	} 

	conceptBuf, err := json.Marshal(conceptJson); 
	if err != nil {
		errChan.Errors = append(errChan.Errors, ErrorNode {
			Err: err, 
			Request: nil, 
		})

		return errChan   
	} 

	headingBuf, err := json.Marshal(headingJson); 
	if err != nil {
		errChan.Errors = append(errChan.Errors, ErrorNode {
			Err: err, 
			Request: nil, 
		})

		return errChan   
	} 

	topicReader := bytes.NewReader(topicBuf); 
	headingReader := bytes.NewReader(headingBuf); 
	conceptReader := bytes.NewReader(conceptBuf); 

	topicRequest, err := http.NewRequest(
		http.MethodPost, 
		url + "/modify_branch", 
		topicReader, 
	) 
	conceptRequest, err := http.NewRequest(
		http.MethodPost, 
		url + "/modify_branch", 
		conceptReader, 
	) 

	headingRequest, err := http.NewRequest(
		http.MethodPost, 
		url + "/modify_branch", 
		headingReader, 
	) 

	requests := [] *http.Request { topicRequest, headingRequest, conceptRequest }; 
	var wg sync.WaitGroup; 

	for _, request := range requests {
		go func () {
			defer wg.Done(); 
			res, err := client.Do(request); 
			if err != nil {
				errChan.AddErrorNode(ErrorNode{
					Err: 	err, 
					Request: request, 
				}); 

			} 

			if res.StatusCode != http.StatusOK {
				errChan.AddErrorNode(ErrorNode{
					Err: 	fmt.Errorf("error : %s", err.Error()), 
					Request: request, 
				}); 
			} 
		}()  
	} 

	wg.Wait(); 

	return errChan; 

} 
