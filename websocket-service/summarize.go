package main 

import (
	"sync" 

	summarizer "openeyesastra/project-astra/summarizer"
) 


func (pm *ProcessMetadata) Summarize(url string, chapters *ChapterNameList) *summarizer.ProcHistory {
	var wg sync.WaitGroup; 
	var request summarizer.SummarizationRequestModel; 
	procHistory := summarizer.ProcHistory{ ProcessStatus: make(map[string] error) }; 
	for _, title := range chapters.Titles {
		wg.Add(1); 
		go func() {
			request = summarizer.SummarizationRequestModel{
				FileName: pm.FileName, 
				EmailId: pm.EmailId, 
				LanguageCode: pm.LanguageCode, 
				ChapterName: title, 
			} 

			defer wg.Done(); 
			summarizer.GenerateSummary(&procHistory, url, &request); 
		}()  
	}

	wg.Wait(); 
	return &procHistory;  
} 
