import time
import json
from fastapi.testclient import TestClient
from main import app
import pytest
import json
from unittest.mock import Mock, patch
from typing import List

client = TestClient(app)

# def test_long_text_exceeds_limit(client):
#     # Create a very long text exceeding the MAX_TEXT_LENGTH limit
#     long_text = "Test sentence. " * 5001  # 5001 sentences, each ~10 characters → ~50010 characters
    
#     # Mock the bucket and file operations
#     mock_blob = Mock()
#     mock_file = Mock()
#     mock_file.__enter__ = Mock(return_value=Mock(read=lambda: json.dumps([{"text": long_text}])))
#     mock_file.__exit__ = Mock(return_value=None)
#     mock_blob.open = Mock(return_value=mock_file)

#     with patch("main.bucket.blob", return_value=mock_blob):
#         # Send the POST request to the endpoint
#         response = client.post(
#             "/summarize",
#             json={
#                 "filename": "test.pdf",
#                 "email_id": "test@test.com",
#                 "chapter_name": "chapter1",
#                 "language_code": "en"
#             }
#         )
    
#     # Assert that the response status code is 413
#     assert response.status_code == 413
    
#     # Assert that the response includes the correct error message
#     assert "exceeds maximum limit" in response.json()["detail"]



##################################################################################################################

# def create_mock_chapter_content(text: str) -> List[dict]:
#     return [{"text": text}]

# class MockBlob:
#     def __init__(self, mock_text: str):
#         self.mock_text = mock_text
    
#     def open(self, mode, retry=None):
#         class MockContextManager:
#             def __init__(self, mock_text):
#                 self.mock_text = mock_text
            
#             def __enter__(self):
#                 return self
            
#             def __exit__(self, *args):
#                 pass
            
#             def read(self):
#                 return json.dumps([{"text": self.mock_text}])
            
#             def write(self, content):
#                 pass
        
#         return MockContextManager(self.mock_text)

# def mock_bucket_response(mock_text: str):
#     return MockBlob(mock_text)

# # Test cases
# def test_summarize_different_languages(mocker, client):
#     # Test data for different languages
#     test_cases = [
#         {
#             "language_code": "en",
#             "text": "This is English text",
#             "expected_status": 200
#         },
#         {
#             "language_code": "es",
#             "text": "Este es un texto en español",
#             "expected_status": 200
#         },
#         {
#             "language_code": "fr",
#             "text": "C'est un texte en français",
#             "expected_status": 200
#         },
#         {
#             "language_code": "invalid",
#             "text": "Some text",
#             "expected_status": 400
#         }
#     ]
    
#     for case in test_cases:
#         # Mock the bucket.blob calls with proper return value
#         mock_blob = mock_bucket_response(case["text"])
#         mocker.patch(
#             "google.cloud.storage.bucket.Bucket.blob",
#             return_value=mock_blob
#         )
        
#         # Mock the summarize_texts function
#         mocker.patch(
#             "main.summarize_texts", 
#             return_value=(True, "Mocked summary", 100)
#         )
        
#         response = client.post(
#             "/summarize",
#             json={
#                 "email_id": "test@example.com",
#                 "filename": "test.pdf",
#                 "chapter_name": "chapter1",
#                 "language_code": case["language_code"]
#             }
#         )
        
#         # Add debug information
#         if response.status_code != case["expected_status"]:
#             print(f"Response status code: {response.status_code}")
#             print(f"Response content: {response.content}")
        
#         assert response.status_code == case["expected_status"]
        
#         if case["expected_status"] == 200:
#             assert response.json()["status"] == True
#             assert "token_count" in response.json()
#         else:
#             assert "detail" in response.json()
#             assert "Invalid language code" in response.json()["detail"]

# def test_mixed_language_content(mocker, client):
#     mixed_text = "This is English mixed with español y français"
    
#     # Mock the bucket.blob calls with proper return value
#     mock_blob = mock_bucket_response(mixed_text)
#     mocker.patch(
#         "google.cloud.storage.bucket.Bucket.blob",
#         return_value=mock_blob
#     )
    
#     mocker.patch(
#         "main.summarize_texts", 
#         return_value=(True, "Mocked summary", 100)
#     )
        
#     response = client.post(
#         "/summarize",
#         json={
#             "email_id": "test@example.com",
#             "filename": "test.pdf",
#             "chapter_name": "chapter1",
#             "language_code": "en"  # Primary language code
#         }
#     )
    
#     if response.status_code != 200:
#         print(f"Response status code: {response.status_code}")
#         print(f"Response content: {response.content}")
    
#     assert response.status_code == 200
#     assert response.json()["status"] == True

###########################################################################################################

# client = TestClient(app)

# @pytest.mark.asyncio
# async def test_summarize_endpoint_timeout():
#     # Mock data that would normally come from the blob
#     mock_chapter_content = [
#         {"text": "This is the first paragraph of test content."},
#         {"text": "This is the second paragraph of test content."}
#     ]
    
#     # Create mock file-like object
#     mock_file = Mock()
#     mock_file.__enter__ = Mock(return_value=Mock())
#     mock_file.__enter__.return_value.read = Mock(return_value=json.dumps(mock_chapter_content))
#     mock_file.__exit__ = Mock(return_value=None)
    
#     # Create mock blob
#     mock_blob = Mock()
#     mock_blob.open = Mock(return_value=mock_file)
    
#     # Create mock bucket
#     mock_bucket = Mock()
#     mock_bucket.blob = Mock(return_value=mock_blob)
    
#     # Test request data
#     test_request = {
#         "filename": "test_document.pdf",
#         "email_id": "test@example.com",
#         "chapter_name": "chapter1",
#         "language_code": "en"
#     }
    
#     # Mock the external dependencies
#     with patch('main.bucket', mock_bucket), \
#          patch('main.summarize_texts', return_value=(True, "Mocked summary", 100)):
        
#         # Record start time
#         start_time = time.time()
        
#         # Send request
#         response = client.post("/summarize", json=test_request)
        
#         # Calculate duration
#         duration = time.time() - start_time
        
#         # Assertions
#         assert response.status_code == 200
#         assert duration <= 30  # Assuming 30 seconds is the acceptable timeout threshold
        
#         # Verify response structure
#         response_data = response.json()
#         assert "time" in response_data
#         assert "token_count" in response_data
#         assert "status" in response_data
#         assert response_data["status"] is True
#         assert response_data["token_count"] == 100




###########################################################################################################################
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app

client = TestClient(app)

# Test data
valid_request = {
    "filename": "test.pdf",
    "email_id": "test@example.com",
    "chapter_name": "chapter1",
    "language_code": "en"
}

@pytest.fixture
def mock_bucket():
    with patch('main.bucket') as mock:
        yield mock

def test_empty_inputs():
    # Test with empty filename
    request1 = valid_request.copy()
    request1["filename"] = ""
    response = client.post("/summarize", json=request1)
    assert response.status_code == 404 
    
    # Test with empty email
    request2 = valid_request.copy()
    request2["email_id"] = ""
    response = client.post("/summarize", json=request2)
    assert response.status_code == 404 
    
    # Test with empty chapter name
    request3 = valid_request.copy()
    request3["chapter_name"] = ""
    response = client.post("/summarize", json=request3)
    assert response.status_code == 404

def test_null_inputs():
    # Test with null filename
    request1 = valid_request.copy()
    request1["filename"] = None
    response = client.post("/summarize", json=request1)
    assert response.status_code == 422
    
    # Test with missing required fields
    response = client.post("/summarize", json={})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_nonexistent_file(mock_bucket):
    mock_blob = Mock()
    mock_blob.open.side_effect = FileNotFoundError("File not found")
    mock_bucket.blob.return_value = mock_blob
    
    response = client.post("/summarize", json=valid_request)
    assert response.status_code == 404
    assert "FileNotFoundError" in response.json()["detail"]

def test_error_message():
    request1 = valid_request.copy()
    request1["filename"] = ""
    response = client.post("/summarize", json=request1)
    assert response.status_code == 404
    assert "Error" in response.json()["detail"]

#########################################################################################################################