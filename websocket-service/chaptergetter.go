package main 

import (
	"net/http"
	"io"
	"encoding/json" 
	"fmt" 
)

type ChapterNameList struct {
	Titles [] string `json:"titles"`
} 

func (pm *ProcessMetadata) ChapterGetter(url string, chapterList *ChapterNameList) error {
	client := &http.Client{}; 
	getUrl := fmt.Sprintf("%s/book_chapters/%s/%s", url, pm.EmailId, pm.FileName); 
	request, err := http.NewRequest(http.MethodGet, getUrl, nil); 
	if err != nil {
			return err; 
	} 
	res, err := client.Do(request); 
	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("%s", http.StatusText(res.StatusCode)); 
	} 
	
	if err != nil {
		return err 
	} 
	
	requestBody, err := io.ReadAll(res.Body); 
	if err != nil {
		return err 
	} 

	json.Unmarshal(requestBody, chapterList); 
	return nil; 
} 
