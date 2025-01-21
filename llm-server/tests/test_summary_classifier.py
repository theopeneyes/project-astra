
# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import Mock, patch
# from main import app

# client = TestClient(app)

# # Test data
# valid_request = {
#     "filename": "test.pdf",
#     "email_id": "test@example.com",
#     "chapter_name": "chapter1",
#     "language_code": "en"
# }

# @pytest.fixture
# def mock_bucket():
#     with patch('main.bucket') as mock:
#         yield mock

# def test_empty_inputs():
#     # Test with empty filename
#     request1 = valid_request.copy()
#     request1["filename"] = ""
#     response = client.post("/summary_classifier", json=request1)
#     assert response.status_code == 404 
    
#     # Test with empty email
#     request2 = valid_request.copy()
#     request2["email_id"] = ""
#     response = client.post("/summary_classifier", json=request2)
#     assert response.status_code == 404 
    
#     # Test with empty chapter name
#     request3 = valid_request.copy()
#     request3["chapter_name"] = ""
#     response = client.post("/summary_classifier", json=request3)
#     assert response.status_code == 404

# def test_null_inputs():
#     # Test with null filename
#     request1 = valid_request.copy()
#     request1["filename"] = None
#     response = client.post("/summary_classifier", json=request1)
#     assert response.status_code == 422
    
#     # Test with missing required fields
#     response = client.post("/summary_classifier", json={})
#     assert response.status_code == 422

# @pytest.mark.asyncio
# async def test_nonexistent_file(mock_bucket):
#     mock_blob = Mock()
#     mock_blob.open.side_effect = FileNotFoundError("File not found")
#     mock_bucket.blob.return_value = mock_blob
    
#     response = client.post("/summary_classifier", json=valid_request)
#     assert response.status_code == 404
#     assert "FileNotFoundError" in response.json()["detail"]

# def test_error_message():
#     request1 = valid_request.copy()
#     request1["filename"] = ""
#     response = client.post("/summary_classifier", json=request1)
#     assert response.status_code == 404
#     assert "Error" in response.json()["detail"]

##############################################################################################################################

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, mock_open
from io import StringIO
from main import app
from exceptions import AmbiguousClassificationError

client = TestClient(app)

def test_ambiguous_classification():
    # Mock data
    test_data = {
        "filename": "test_file.pdf",
        "email_id": "test@example.com",
        "chapter_name": "chapter1",
        "language_code": "en"
    }
    
    # Create mock content
    mock_content = """
    This is an ambiguous text that could be classified in multiple ways.
    It contains elements that might overlap between different categories.
    """
    
    # Create a mock file object
    mock_file = StringIO(mock_content)
    
    # Mock the blob operations
    mock_blob = Mock()
    mock_blob.open = mock_open(read_data=mock_content)
    
    with patch('main.bucket') as mock_bucket:
        mock_bucket.blob.return_value = mock_blob
        
        # Mock generate_chapter_metadata to simulate ambiguous classification
        with patch('main.generate_chapter_metadata') as mock_generate:
            mock_generate.side_effect = AmbiguousClassificationError()
            
            # Make request to endpoint
            response = client.post("/summary_classifier", json=test_data)
            
            # Check if the response indicates the ambiguous classification error
            assert response.status_code == 400
            assert "AmbiguousClassificationError" in response.json()["detail"]