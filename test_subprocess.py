import requests 
import json 

response = requests.post(
        "http://localhost:8000/run_subprocess", 
        json = {
            "email_id" : "pratyush.rao@gmail.com", 
            "filename" : "ml.pdf",  
        } 

)

if response.status_code == 200: 
    print(json.dumps(response.json(), indent=4)) 
else: 
    print("Something went wrong fs. Skill issues.") 
