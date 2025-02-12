package main 

import (
	"net/http"  
	"io"  
	"fmt" 
	"sync" 
	"bytes" 
	"encoding/json"
) 

type FeedbackDefinition struct {
	Request 	*http.Request 
	NodeId 		int 
	ChapterName 	string 
	Err 		error 
	Description	string 
} 

type NodeCountResponse struct {
	FileName 	string 
	ChapterName 	string 
	EmailId 	string 
	NodeCount 	int 
} 

type RewriteJsonRequestModel struct {
	FileName 	string 	`json:"filename"` 
	ChapterName 	string 	`json:"chapter_name"` 
	EmailId 	string 	`json:"email_id"` 
	NodeID 		int 	`json:"node_id"` 
	LanguageCode 	string 	`json:"language_code"` 
} 

type SynthesizeSeriesRequestModel struct {
	FileName 	string 	`json:"filename"` 
	ChapterName 	string 	`json:"chapter_name"`
	EmailId 	string 	`json:"email_id"`
	NodeId		int 	`json:"node_id"`
	BranchName 	string 	`json:"branch_name"` 
} 

type RequestErrors struct {
	mu 		sync.Mutex
	ErrMap		map[string] FeedbackDefinition   
} 

func (rawr *RequestErrors) AddError(chapterName string, fb FeedbackDefinition ) {
	rawr.mu.Lock(); 
	defer rawr.mu.Unlock(); 
	rawr.ErrMap[chapterName] = fb; 
} 

func (pm *ProcessMetadata) RewriteNodes(url, chapterName string, requestErrors *RequestErrors) {
	client := http.Client{}; 
	nodeRequest, err := http.NewRequest(
		http.MethodGet, 
		url + "/" + pm.EmaliId + "/" + pm.FileName + "/" + chapterName, 
		nil, 
	); 
	
	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nil, 
			NodeId 		: -1, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Error while making new Request",  
		});   

		return 
	} 
	

	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nodeRequest, 
			NodeId 		: -1, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Error in getting node data from the new request",  
		});  

		return 
	} 
	
	res, err := client.Do(nodeRequest); 
	if res.StatusCode != http.StatusOK {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nodeRequest, 
			NodeId 		: -1, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Response needs a therapist",  
		});   
	} 

	resBuf, err := io.ReadAll(res.Body); 
	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nodeRequest, 
			NodeId 		: -1, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Response JSON does not match with structure defined",  
		} ); 
	} 
	
	nodeCountResponse := NodeCountResponse {}; 
	err := json.Unmarshal(resBuf, &nodeCountResponse); 
	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nodeRequest, 
			NodeId 		: -1, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Error parsing json response",  
		} ); 
	} 

	
	nc := nodeCountResponse.NodeCount; 
	for i := 0; i < nc; i++ {
		RewriteJson(&requestErrors, nodeId, chapterName); 

		go pm.SynthesizeRelationalStrength(&requestErrors, url, nodeId, chapterName); 
		go pm.SynthesizeRepresentStrength(&requestErrors, nodeId, chapterName); 
		go pm.SynthesizeRepresentDepth(&requestErrors, nodeId, chapterName); 
	} 
} 

func (pm *ProcessMetadata) SynthesizeRelationalStrength(re *RequestErrors, url string, nodeId int, chapterName string) {
	client := http.Client{}; 

	// topics
	topicData := SynthesizeSeriesRequestModel {
		FileName: pm.FileName, 	
		EmailId: pm.EmailId, 
		ChapterName: chapterName, 
		NodeId: nodeId, 
		BranchName: "topic" 
	} 

	topicJson, err := json.Marshal(topicData); 
	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nil, 
			NodeId 		: nodeId, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Error parsing struct to json",  
		} ); 
	} 
	topicBuf := bytes.NewReader(topicJson); 
	topicRequest, err := http.NewRequest(
		http.MethodPost, 
		url + "/synthesize/strength/relational", 
		topicBuf, 
	); 
	
	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nil, 
			NodeId 		: nodeId, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Error processing the request",  
		} ); 
	} 

	
	// concepts 
	conceptData := SynthesizeSeriesRequestModel {
		FileName: pm.FileName, 	
		EmailId: pm.EmailId, 
		ChapterName: chapterName, 
		NodeId: nodeId, 
		BranchName: "concept" 
	} 

	conceptJson, err := json.Marshal(conceptData); 
	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nil, 
			NodeId 		: nodeId, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Error parsing struct",  
		} ); 
	} 

	conceptBuf := bytes.NewReader(conceptJson); 
	conceptRequest, err := http.NewRequest(
		http.MethodPost, 
		url + "/synthesize/strength/relational", 
		conceptBuf, 
	); 

	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nil, 
			NodeId 		: nodeId, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Error processing the request",  
		} ); 
	} 


	// headings
	headingsData := SynthesizeSeriesRequestModel {
		FileName: pm.FileName, 	
		EmailId: pm.EmailId, 
		ChapterName: chapterName, 
		NodeId: nodeId, 
		BranchName: "heading_text" 
	} 

	headingsJson, err := json.Marshal(headingsData); 
	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nil, 
			NodeId 		: nodeId, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Error parsing struct",  
		} ); 
	} 

	headingsBuf := bytes.NewReader(headingsJson); 
	headingsRequest, err := http.NewRequest(
		http.MethodPost, 
		url + "/synthesize/strength/relational", 
		headingsBuf, 
	); 

	if err != nil {
		requestErrors.AddError(chapterName, FeedbackDefinition {
			Request 	: nil, 
			NodeId 		: nodeId, 
			ChapterName	: chapterName,  	
			Err		: err, 
			Description 	: "Error Sending request",  
		} ); 
	} 

	
	// lets make the requests now 
	requests := [] *http.request { topicrequest, conceptsrequest, headingsrequest }; 
	for _, request := range requests {
		go func () {
			res, err := client.do(request);  
			if err != nil {
				requesterrors.adderror(chaptername, feedbackdefinition {
					request 	: request, 
					nodeid 		: nodeid, 
					chaptername	: chaptername,  	
					err		: err, 
					description 	: "error in request",  
				} ); 
			}
			

			if res.StatusCode != http.StatusOK {
				requesterrors.adderror(chaptername, feedbackdefinition {
					request 	: request, 
					nodeid 		: nodeid, 
					chaptername	: chaptername,  	
					err		: err, 
					description 	: "error in request",  
				} ); 
			}  
		}()  
	} 	
} 
