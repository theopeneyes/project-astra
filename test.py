import requests 
import os 

# reading a test pdfs from the endpoint  
PDF_BASE_PATH: str = "pdfs" 
API_URL: str = "http://127.0.0.1:8000"

def test_data_loader() -> None: 
    if not os.listdir(PDF_BASE_PATH): return 
    for pdf_filename in os.listdir(PDF_BASE_PATH): 
        with open(os.path.join(PDF_BASE_PATH, pdf_filename), "rb") as f: 
            byte_content = f.read() # reading the content in bytes 

        # test if the files are working 
        files = {
            "pdf_file": (pdf_filename, byte_content, "application/pdf"), 
        }

        response = requests.post(API_URL + "/data_loader", files=files)
        assert isinstance(response.json(), list)
    
    files = {
        "pdf_file": (pdf_filename, b'', "image/jpeg")
    }

    # test if the http error occurs correctly 
    response = requests.post(API_URL + "/data_loader", files=files, timeout=300 )
    assert response.status_code == 400  

if __name__ == '__main__': 
    test_data_loader()
