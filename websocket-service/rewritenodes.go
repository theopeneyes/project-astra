package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"sync"
)

type FeedbackDefinition struct {
	Request     *http.Request
	NodeId      int
	ChapterName string
	Err         error
	Description string
}

type NodeCountResponse struct {
	FileName    string `json:"filename"`
	ChapterName string `json:"chapter_name"`
	EmailId     string `json:"email_id"`
	NodeCount   int    `json:"node_count"`
}

type RewriteJsonRequestModel struct {
	FileName     string `json:"filename"`
	ChapterName  string `json:"chapter_name"`
	EmailId      string `json:"email_id"`
	NodeId       int    `json:"node_id"`
	LanguageCode string `json:"language_code"`
}

type SynthesizeSeriesRequestModel struct {
	FileName    string `json:"filename"`
	ChapterName string `json:"chapter_name"`
	EmailId     string `json:"email_id"`
	NodeId      int    `json:"node_id"`
	BranchName  string `json:"branch_name"`
}

type RequestErrors struct {
	mu     sync.Mutex
	ErrMap map[string]FeedbackDefinition
}

func (rawr *RequestErrors) AddError(chapterName string, fb FeedbackDefinition) {
	rawr.mu.Lock()
	defer rawr.mu.Unlock()
	rawr.ErrMap[chapterName] = fb
}

func (pm *ProcessMetadata) RewriteNodes(url, chapterName string, re *RequestErrors) {

	client := &http.Client{}
	nodeRequest, err := http.NewRequest(
		http.MethodGet,
		url+"/"+"get_node_count"+"/"+pm.EmailId+"/"+pm.FileName+"/"+chapterName,
		nil,
	)

	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nil,
			NodeId:      -1,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error while making new Request",
		})

		return
	}

	res, err := client.Do(nodeRequest)
	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nodeRequest,
			NodeId:      -1,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error in getting node data from the new request",
		})

		return
	}

	if res.StatusCode != http.StatusOK {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nodeRequest,
			NodeId:      -1,
			ChapterName: chapterName,
			Err:         err,
			Description: "Response needs a therapist",
		})
	}

	resBuf, err := io.ReadAll(res.Body)
	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nodeRequest,
			NodeId:      -1,
			ChapterName: chapterName,
			Err:         err,
			Description: "Response JSON does not match with structure defined",
		})
	}

	nodeCountResponse := NodeCountResponse{}
	err = json.Unmarshal(resBuf, &nodeCountResponse)
	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nodeRequest,
			NodeId:      -1,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error parsing json response",
		})
	}

	nc := nodeCountResponse.NodeCount
	var wg sync.WaitGroup
	for i := 0; i < nc; i++ {
		nodeId := i
		pm.RewriteJson(re, url, nodeId, chapterName)

		wg.Add(1)
		go func(nodeId int, chapterName string) {
			defer wg.Done()
			pm.Synthesize(
				re,
				url+"/synthesize/strength/relational",
				nodeId,
				chapterName,
			)
		}(nodeId, chapterName)

		wg.Add(1)
		go func(nodeId int, chapterName string) {
			defer wg.Done()
			pm.Synthesize(
				re,
				url+"/synthesize/depth/representational",
				nodeId,
				chapterName,
			)
		}(nodeId, chapterName)

		wg.Add(1)
		go func(nodeId int, chapterName string) {
			defer wg.Done()
			pm.Synthesize(
				re,
				url+"/synthesize/strength/representational",
				nodeId,
				chapterName,
			)
		}(nodeId, chapterName)
	}

	wg.Wait()

}

func (pm *ProcessMetadata) RewriteJson(re *RequestErrors, url string, nodeId int, chapterName string) {
	client := &http.Client{}

	log.Println("Rewrite json chalra")
	rewriteData := RewriteJsonRequestModel{
		FileName:     pm.FileName,
		EmailId:      pm.EmailId,
		LanguageCode: pm.LanguageCode,
		NodeId:       nodeId,
		ChapterName:  chapterName,
	}

	rewriteBuf, err := json.Marshal(rewriteData)
	if err != nil {
		log.Printf("Maybe got error in rewrite json who's to say: %d and chapter name : %s, Error: %s\n", nodeId, chapterName, err.Error())
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nil,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error processing the request",
		})

		return
	}

	rewriteReader := bytes.NewReader(rewriteBuf)
	rewriteRequest, err := http.NewRequest(
		http.MethodPost,
		url+"/rewrite_json",
		rewriteReader,
	)

	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nil,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error processing the request",
		})

		return
	}

	res, err := client.Do(rewriteRequest)
	if res.StatusCode != http.StatusOK {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     rewriteRequest,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         fmt.Errorf("status code : %d, error text: %s", res.StatusCode, http.StatusText(res.StatusCode)),
			Description: "Error processing the request",
		})

		return
	}

	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     rewriteRequest,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error processing the request",
		})

		return
	}
}

func (pm *ProcessMetadata) Synthesize(re *RequestErrors, url string, nodeId int, chapterName string) {
	client := &http.Client{}

	// topics
	topicData := SynthesizeSeriesRequestModel{
		FileName:    pm.FileName,
		EmailId:     pm.EmailId,
		ChapterName: chapterName,
		NodeId:      nodeId,
		BranchName:  "topic",
	}

	topicJson, err := json.Marshal(topicData)
	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nil,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error parsing struct to json",
		})

		return
	}

	topicBuf := bytes.NewReader(topicJson)
	topicRequest, err := http.NewRequest(
		http.MethodPost,
		url,
		topicBuf,
	)

	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nil,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error processing the request",
		})

		return
	}

	// concepts
	conceptData := SynthesizeSeriesRequestModel{
		FileName:    pm.FileName,
		EmailId:     pm.EmailId,
		ChapterName: chapterName,
		NodeId:      nodeId,
		BranchName:  "concept",
	}

	conceptJson, err := json.Marshal(conceptData)
	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nil,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error parsing struct",
		})
	}

	conceptBuf := bytes.NewReader(conceptJson)
	conceptRequest, err := http.NewRequest(
		http.MethodPost,
		url,
		conceptBuf,
	)

	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nil,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error processing the request",
		})

		return
	}

	// headings
	headingsData := SynthesizeSeriesRequestModel{
		FileName:    pm.FileName,
		EmailId:     pm.EmailId,
		ChapterName: chapterName,
		NodeId:      nodeId,
		BranchName:  "heading_text",
	}

	headingsJson, err := json.Marshal(headingsData)
	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nil,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error parsing struct",
		})

		return
	}

	headingsBuf := bytes.NewReader(headingsJson)
	headingsRequest, err := http.NewRequest(
		http.MethodPost,
		url,
		headingsBuf,
	)

	if err != nil {
		re.AddError(chapterName, FeedbackDefinition{
			Request:     nil,
			NodeId:      nodeId,
			ChapterName: chapterName,
			Err:         err,
			Description: "Error Sending request",
		})
	}

	// lets make the requests now
	requests := []*http.Request{topicRequest, conceptRequest, headingsRequest}
	var wg sync.WaitGroup
	for _, request := range requests {
		wg.Add(1)
		go func(request *http.Request) {
			defer wg.Done()
			res, err := client.Do(request)
			if err != nil {
				re.AddError(chapterName, FeedbackDefinition{
					Request:     request,
					NodeId:      nodeId,
					ChapterName: chapterName,
					Err:         err,
					Description: "error in request",
				})

				return

			}

			if res.StatusCode != http.StatusOK {
				re.AddError(chapterName, FeedbackDefinition{
					Request:     request,
					NodeId:      nodeId,
					ChapterName: chapterName,
					Err:         err,
					Description: "error in request",
				})

				return
			}
		}(request)
	}

	wg.Wait()
}
