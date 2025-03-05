package main 

import (
	"fmt"
	"flag"
	"log" 
	"slices" 
	"sync" 
) 

type ProcessMetadata struct {
	FileName string 
	EmailId string 
	LanguageCode string 
} 

func NewProcess() *ProcessMetadata {
	return &ProcessMetadata{}; 
} 

const LlmServerURL string = "http://localhost:8000"; 

func main() {
	// setting command line arguments to their respective variables. 
	pm := NewProcess(); 
	flag.StringVar(
		&pm.FileName, 
		"filename", 
		"...", 
		"Enter the name of the file that you wish to process. The file should already be uploaded within cloud", 
	); 	
	
	flag.StringVar(
		&pm.EmailId, 
		"emailId", 
		"...", 
		"Enter the email Id of the registered user for authentication", 
	);  
	
	flag.Parse(); 
	
	// fmt.Printf("the struct is as follows: %+v\n", pm); 
	if pm.FileName == "..." {
		panic(fmt.Errorf("issue with parsing the file name you provided. Read the help and provide the inputs appropriately")); 
	} 

	if pm.EmailId == "..." {
		panic(fmt.Errorf("issue with parsing the email id you provided. Read the help and provide the inputs appropriately"));  
	} 
	
	languageCode, err := pm.DataLoader(); 
	if err != nil {
        	log.Printf("Error occured while parsing in the data loader: %+v\n", 
		 err.Error()); 
	} 
	
	pm.LanguageCode = languageCode; 
	
	// access each chapter name 
	chapters := ChapterNameList{}; 
	pm.ChapterGetter(LlmServerURL, &chapters); 

	// getting names of chapters  
	log.Printf("Starting to summarize and classify json..."); 
	procHistory := pm.Summarize(LlmServerURL, &chapters); 

	log.Printf("Process history accessed! %+v\n", procHistory.ProcessStatus); 

	chaptersFailed := ChapterNameList{}; 
	chaptersFailed.Titles = make([] string, 0); 
	
	for processId, err := range procHistory.ProcessStatus {
		if err != nil {
			chaptersFailed.Titles = append(chaptersFailed.Titles, processId); 	
		} 
	} 
	
	log.Printf("Total count of failed titles are as follows: %d\n", len(chaptersFailed.Titles)); 
	log.Printf("Retrying failed titles...\n"); 

	// retrying the endpoint 
	procHistory = pm.Summarize(LlmServerURL, &chaptersFailed); 

	chaptersFailed = ChapterNameList{}; 
	chaptersFailed.Titles = make([] string, 0); 
	for processId, err := range procHistory.ProcessStatus {
		if err != nil {
			chaptersFailed.Titles = append(chaptersFailed.Titles, processId); 	
		} 
	} 


	log.Printf("Total count of failed titles in retry are as follows: %d\n", len(chaptersFailed.Titles)); 
	
	// now let's get the node count 
	chaptersSucceded := ChapterNameList{}; 
	for _, chapterName := range chapters.Titles {
		if !slices.Contains(chaptersFailed.Titles, chapterName) {
			chaptersSucceded.Titles = append(chaptersSucceded.Titles, chapterName);  
		} 
	} 

	re := RequestErrors {
		ErrMap : make(map[string] FeedbackDefinition), 
	} 

	
	var wg sync.WaitGroup; 
	for _, chapterName := range chapters.Titles {
		log.Printf("sending go-routines to parse chapter: %s\n", chapterName); 
		wg.Add(1); 
		go func(chapterName string) {
			defer wg.Done(); 
			pm.RewriteNodes(LlmServerURL, chapterName, &re); 
		}(chapterName)  
	} 
	wg.Wait(); 
	log.Println("Done parsing chapters"); 

	err = pm.Preprocess(LlmServerURL); 
	if err != nil {
		panic(err); 
	} 

	err = pm.Segregate(LlmServerURL); 
	if err != nil {
		panic(err); 
	} 

	pm.Modify(LlmServerURL); 

	err = pm.AddWordCount(LlmServerURL); 
	if err != nil {
		panic(err); 
	} 

	err = pm.SendEmailToClient(LlmServerURL); 
	if err != nil {
		panic(err)
	} 
} 
