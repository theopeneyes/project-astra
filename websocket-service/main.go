package main 

import (
	"fmt"
	"flag"
	"log" 
) 

type ProcessMetadata struct {
	FileName string 
	EmailId string 
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
		fmt.Errorf("Issue with parsing the file name you provided. Read the help and provide the inputs appropriately\n"); 
	} 

	if pm.EmailId == "..." {
		fmt.Errorf("Issue with parsing the email id you provided. Read the help and provide the inputs appropriately\n"); 
	} 
	
	err := pm.DataLoader(); 
	if err != nil {
		log.Printf("Error occured while parsing in the data loader: %+v\n", err.Error()); 
	} 

	// Data Loader running sequentially  
} 
