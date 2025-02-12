package main 

import (
	"sync" 

	summarizer "openeyesastra/project-astra/summarizer"
) 


func (pm *ProcessMetadata) Summarize(url string, chapters *ChapterNameList) *summarizer.ProcHistory {
	var wg sync.WaitGroup; 
	procHistory := summarizer.ProcHistory{ ProcessStatus: make(map[string] error) }; 
	for _, title := range chapters.Titles {
		wg.Add(1); 
		go func(title string) {
			request := summarizer.SummarizationRequestModel{
				FileName: pm.FileName, 
				EmailId: pm.EmailId, 
				LanguageCode: pm.LanguageCode, 
				ChapterName: title, 
			} 

			defer wg.Done(); 
			summarizer.GenerateSummary(&procHistory, url, request); 
		}(title)  
	}

	wg.Wait(); 
	return &procHistory;  
} 
