package summarizer 

import (
	"bytes" 
	"encoding/json" 
	"net/http" 
	"sync" 
	"fmt" 
) 

type SummarizationRequestModel struct {
	EmailId 	string `json:"email_id"`
	FileName 	string `json:"filename"`
	LanguageCode 	string `json:"language_code"`
	ChapterName 	string `json:"chapter_name"`
} 


type ProcHistory struct {
	mu 		sync.Mutex 
	ProcessStatus 	map[string] error 
} 

func (ph *ProcHistory) SetProcessStatus(title string, err error) {
	ph.mu.Lock(); 
	defer ph.mu.Unlock(); 
	ph.ProcessStatus[title] = err; 
} 

func GenerateSummary(proc *ProcHistory, url string, request SummarizationRequestModel) {
	client := &http.Client{}; 
	requestJsonBuff, err := json.Marshal(request); 
	if err != nil {
		proc.SetProcessStatus(request.ChapterName, err); 
		return 
	} 

	reader := bytes.NewReader(requestJsonBuff); 
	requestSummary, err := http.NewRequest(
		http.MethodPost, 
		url + "/chapter_loader", 
		reader, 
	);  

	if err != nil {
		proc.SetProcessStatus(request.ChapterName, err); 
		return 
	} 

	res, err := client.Do(requestSummary); 
	if err != nil {
		proc.SetProcessStatus(request.ChapterName, err); 
		return 
	} 

	if res.StatusCode != http.StatusOK {
		err = fmt.Errorf("%s", http.StatusText(res.StatusCode)); ; 
		proc.SetProcessStatus(request.ChapterName, err); 
		return  
	} 

	readerSummarize := bytes.NewReader(requestJsonBuff); 
	requestSummarySummarizer, err := http.NewRequest(
		http.MethodPost, 
		url + "/summarize", 
		readerSummarize, 
	);  

	if err != nil {
		proc.SetProcessStatus(request.ChapterName, err); 
		return 
	} 

	res, err = client.Do(requestSummarySummarizer); 
	if err != nil {
		proc.SetProcessStatus(request.ChapterName, err); 
		return 
	} 

	if res.StatusCode != http.StatusOK {
		err = fmt.Errorf("%s", http.StatusText(res.StatusCode)); ; 
		proc.SetProcessStatus(request.ChapterName, err); 
		return  
	} 

	readerClassify := bytes.NewReader(requestJsonBuff); 
	requestSummaryClassifier, err := http.NewRequest(
		http.MethodPost, 
		url + "/summary_classifier", 
		readerClassify, 
	);  

	if err != nil {
		proc.SetProcessStatus(request.ChapterName, err); 
		return 
	} 

	res, err = client.Do(requestSummaryClassifier); 
	if err != nil {
		proc.SetProcessStatus(request.ChapterName, err); 
		return 
	} 

	if res.StatusCode != http.StatusOK {
		err = fmt.Errorf("%s", http.StatusText(res.StatusCode)); ; 
		proc.SetProcessStatus(request.ChapterName, err); 
		return 
	} 
	
	proc.SetProcessStatus(request.ChapterName, nil); 	
} 
