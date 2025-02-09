package main;  

import (
	"fmt" 
	"log" 

	loader "openeyesastra/project-astra/dataloader"  
) 


func (pm *ProcessMetadata) DataLoader() error {
	baseRequestJson := loader.BaseRequestModel {
		FileName: pm.FileName, 
		EmailId: pm.EmailId, 
	};  

	log.Println("Initiated process of converting pdf and getting pages.."); 

	pageCh := make(chan loader.PageCountResponseCh); 
	errCh := make (chan error); 
	go loader.RunPdfConverter(LlmServerURL, errCh, baseRequestJson);  
	go loader.AccessPageCount(LlmServerURL, pageCh, baseRequestJson);  

	err := <- errCh; 
	pageResponse := <- pageCh; 

	if err != nil {
		return err; 
	} 
	
	if pageResponse.Error != nil {
		return pageResponse.Error; 
	} 
	
	if pageResponse.PageCount > 20 {
		pageResponse.PageCount = 20; 
	} 

	log.Println("Converting and page count getting complete."); 
	log.Println("Getting Language codes..."); 

	languageCode, err := loader.DetectLanguage(LlmServerURL, baseRequestJson); 
	if err != nil {
		return err; 
	} 

	fmt.Printf("The language code : %s\n", languageCode); 
	log.Println("Language codes accessed!"); 
	
	log.Println("running chapter wise segmentation..."); 
	
	extractContentsPageJson := loader.ExtractContentsPageRequestModel{
		FileName: pm.FileName, 
		EmailId: pm.EmailId, 
		PageNumbers: pageResponse.PageCount,  
		LanguageCode: languageCode, 
	} 
	
	err = loader.RunChapterWiseSegmentation(LlmServerURL, extractContentsPageJson); 
	if err != nil {
		return nil; 
	} 
	
	log.Println("Chapter reformation ran successfully!"); 
	return nil; 
} 
	


