package main 

import (
	"fmt"
	"net/http"
	"encoding/json"
	"bytes"
	"log" 
)   

const LlmServerUrl string = "http://localhost:8000"; 
const emailId string = "test.fifth@yahoo.com"; 
var GetStatusUrl string = fmt.Sprintf("%s/%s", LlmServerUrl, "get_status"); 

type GetStatusRequestModel struct {
	emailId string `json:email_id`
} 

type StatusResponseModel struct {
	FileName string `json:file_name`
	CreatedOn string `json:created_on`
	StatusId int `json:status_id`
	Status string `json:status`
} 


// routing apps 
func GetStatusOfService(w http.ResponseWriter, r *http.Request) {
	getStatusBody := GetStatusRequestModel{
		emailId: emailId, 
	} 
	
	defer log.Printf("%d OK /getStatus SUCCESS\n", http.StatusOK); 

	requestContent, err := json.Marshal(getStatusBody); 
	if err != nil {
		log.Printf("%d FR /getStatus FAILURE\n", http.StatusInternalServerError); 
		http.Error(w, err.Error(), http.StatusInternalServerError);  
		return 
	} 

	getStatusBodyReader := bytes.NewReader(requestContent);  
	request, err := http.NewRequest(http.MethodGet, GetStatusUrl, getStatusBodyReader);  
	request.Header.Set("Content-Type", "application/json"); 
	client := &http.Client{}; 
	response, err := client.Do(request); 

	if err != nil {	
		log.Printf("%d FR /getStatus FAILURE\n", http.StatusInternalServerError); 
		http.Error(w, err.Error(), http.StatusInternalServerError); 
		return 
	}
	
	statusVector := make([] StatusResponseModel); 
	json.Unmarshal(&statusVector, response); 
	fmt.Printf(response); 
		
} 


func main() {
	// router 
	mux := http.NewServeMux(); 
	mux.HandleFunc("GET /getStatus", GetStatusOfService);  
	server := &http.Server {
		Addr: ":6969", 
		Handler: mux, 
	}  

	log.Printf("Listening to service at port http://localhost:6969..."); 	
	err := server.ListenAndServe(); 
	if err != nil {
		log.Printf("Could not listen the server do to the following error : %s\n", err.Error()); 
	} 
}  
