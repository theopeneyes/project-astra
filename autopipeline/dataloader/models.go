package dataloader; 

type BaseRequestModel struct {
	FileName 	string `json:"filename"`
	EmailId 	string `json:"email_id"`
} 

type PageCountResponseModel struct {
	FileName 	string `json:"filename"`
	EmailId 	string `json:"email_id"` 
	Time 		float32 `json:"time"`
	PageCount	int32 `json:"page_count"`
} 

type PageCountResponseCh struct {
	Error 		error 
	PageCount 	int32
} 

type LanguageResponseModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	TokenCount 	int32 	`json:"token_count"`
	Time 		float32 `json:"time"`
	LanguageCode 	string `json:"detected_language"`
	Confidence 	float32 `json:"confidence"`
}

type ExtractContentsPageRequestModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	LanguageCode 	string 	`json:"language_code"`
	PageNumbers 	int32 	`json:"number_of_pages"`
} 

type ExtractContentsPageResponseModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	TokenCount 	int32 	`json:"token_count"`
	Time 		float32 `json:"time"`
	FirstPage 	int32 	`json:"first_page"`
	LastPage 	int32 	`json:"last_page"`
} 

type ChapterPageRequestModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	FirstPage 	int32 	`json:"first_page"`
	LastPage 	int32 	`json:"last_page"`
	LanguageCode 	string 	`json:"language_code"`
} 


type ChapterPageResponseModel struct {
	FileName 	string 	`json:"filename"`
	EmailId 	string 	`json:"email_id"`
	Time 		float32 `json:"time"`
	TokenCount 	int32 	`json:"token_count"`
} 
