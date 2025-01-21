import time
import pytest_asyncio
import pytest
import json
import pandas as pd
import unittest

from io import StringIO
from main import chapter_loader, app
from fastapi import HTTPException
from fastapi.testclient import TestClient
from google.cloud.exceptions import GoogleCloudError
from google.cloud.exceptions import TransientError
from unittest.mock import Mock, patch, MagicMock


client = TestClient(app)


@pytest.fixture
def sample_request():
    class Request:
        email_id = "test@example.com"
        filename = "test_book.pdf"
        chapter_name = "chapter1"
        language_code = "en"
    return Request()

@pytest.mark.asyncio
@patch('main.bucket')
async def test_chapter_loader_file_upload_failure(mock_bucket, sample_request):
    # Create a mock blob that raises GoogleCloudError
    mock_blob = Mock()
    mock_context = Mock()
    mock_context.__enter__ = Mock(side_effect=GoogleCloudError("Failed to access file"))
    mock_context.__exit__ = Mock(return_value=False)
    mock_blob.open.return_value = mock_context
    
    # Configure the bucket mock to return our configured blob mock
    mock_bucket.blob.return_value = mock_blob
    
    with pytest.raises(HTTPException) as exc_info:
        await chapter_loader(sample_request)
    
    assert exc_info.value.status_code == 503
    assert "Upload failed: Unable to access file" in str(exc_info.value.detail)

    

@pytest.mark.asyncio
@patch('main.bucket')
async def test_chapter_loader_invalid_json_format(mock_bucket, sample_request):
    # Create mock blob that returns invalid JSON
    mock_blob = Mock()
    mock_file = Mock()
    mock_file.read.return_value = "{ invalid json }"  # This will cause JSONDecodeError
    
    # Mock the context manager
    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_file)
    mock_context.__exit__ = Mock(return_value=None)
    mock_blob.open.return_value = mock_context
    
    # Configure bucket mock to return our blob mock
    mock_bucket.blob.return_value = mock_blob
    
    with pytest.raises(HTTPException) as exc_info:
        await chapter_loader(sample_request)
    
    assert exc_info.value.status_code == 400
    assert "Invalid JSON format in chapter_to_heading.json" in str(exc_info.value.detail)

    


def test_corrupted_pdf():
    """Test handling of corrupted PDF file"""
    client = TestClient(app)
    test_request = {
        "email_id": "test@example.com",
        "filename": "test_book.pdf",
        "chapter_name": "chapter1",
        "language_code": "en"
    }

    # Mock the bucket and blob to simulate a corrupted PDF
    with patch('main.bucket') as mock_bucket:
        mock_blob = Mock()
        mock_blob.open.side_effect = GoogleCloudError("Invalid or corrupted PDF file")
        mock_bucket.blob.return_value = mock_blob
        
        # Test the endpoint
        response = client.post("/chapter_loader", json=test_request)
        
        # Assert the response
        assert response.status_code == 503
        assert "Unable to access file" in response.json()["detail"]





def test_large_file_handling():
  """Test handling of large files"""
  client = TestClient(app)
  test_request = {
      "email_id": "test@example.com",
      "filename": "large_file.pdf",
      "chapter_name": "chapter1",
      "language_code": "en"
  }

  # Mock the blob to simulate a large file size
  with patch("main.bucket") as mock_bucket:
      mock_blob = Mock()
      mock_blob.size = 200 * 1024 * 1024  # Simulate a 200 MB file
      mock_bucket.blob.return_value = mock_blob

      # Call the endpoint
      response = client.post("/chapter_loader", json=test_request)
      print(response.json()["detail"])
      # Assert the error code and detailed message related to file size
      assert response.status_code == 413
      assert "File is too large" in response.json()["detail"]

  # Add an additional assertion to check for unexpected errors
  assert "Error:" not in response.json()["detail"], "Unexpected error occurred"




# def test_incorrect_data_parsing():
#     client = TestClient(app)

#     # Mock the blobs and their responses
#     with patch("google.cloud.storage.Blob.open") as mock_open:
#         # Mock JSON file with invalid JSON
#         mock_open.return_value.__enter__.side_effect = [
#             MagicMock(read=lambda: "{\"key\": \"value\","),  # Invalid JSON
#             MagicMock(read=lambda: "col1,col2\n1,a\n2,b"),        # Valid CSV
#             MagicMock(read=lambda: "{\"images\": [\"img1\", \"img2\"]}")  # Valid JSON
#         ]

#         # Define a request payload
#         payload = {
#             "email_id": "test@example.com",
#             "filename": "test_file.pdf",
#             "chapter_name": "Chapter1",
#             "language_code": "en"
#         }

#         # Send POST request to the endpoint
#         response = client.post("/chapter_loader", json=payload)

#         # Check response for invalid JSON error
#         assert response.status_code == 400
#         assert "Invalid JSON format in chapter_to_heading.json" in response.json()["detail"]



@pytest.fixture
def mock_bucket():
    """Mock the storage bucket and its methods."""
    mock_blob = MagicMock()
    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    return mock_bucket

@patch("main.bucket")  # Replace 'your_module' with the actual module path where 'bucket' is defined
def test_chapter_loader_incorrect_parsing(mock_bucket):
    # Mock blob.open for incorrect file format
    mock_blob = mock_bucket.blob.return_value
    mock_blob.open.side_effect = [
        MagicMock(read=lambda: json.dumps({"chapter1": "heading1"})),  # Valid chapter_to_heading.json
        MagicMock(read=lambda: "chapter_name,some_data\n1,abc\n2,xyz\n"),  # Valid CSV content
        MagicMock(read=lambda: "invalid_json_content"),  # Invalid chapter_images.json
    ]

    # Define the request payload
    request_payload = {
        "email_id": "test@example.com",
        "filename": "test_file.pdf",
        "chapter_name": "Chapter 1",
        "language_code": "en",
    }

    # Send POST request
    response = client.post("/chapter_loader", json=request_payload)

    # Assertions
    assert response.status_code == 404  # Expecting a 404 error due to parsing failure
    assert "Error :" in response.json()["detail"]  # Check if error detail is included


def test_chapter_loader_permission_error():
    # Create request data as a dictionary
    mock_request = {
        "email_id": "test@example.com",
        "filename": "test_book.pdf",
        "chapter_name": "chapter1",
        "language_code": "en"
    }
    
    # Mock the storage bucket and blob
    mock_bucket = Mock()
    mock_blob = Mock()
    
    # Configure the blob to raise a PermissionError when opened
    mock_blob.open = Mock(side_effect=PermissionError("Permission denied"))
    mock_bucket.blob.return_value = mock_blob
    
    # Patch the storage bucket
    with patch('main.bucket', mock_bucket):
        # Test that the function raises an HTTPException
        with pytest.raises(HTTPException) as exc_info:
            chapter_loader(mock_request)
        
        # Verify the error details
        assert exc_info.value.status_code == 404
        assert "Error :PermissionError" in exc_info.value.detail

    
class TestChapterLoader(unittest.TestCase):
    def setUp(self):
        self.test_request = {
            "email_id": "test@example.com",
            "filename": "test_book.pdf",
            "chapter_name": "chapter1",
            "language_code": "en"
        }

    @patch('google.cloud.storage.blob.Blob')
    def test_network_failure(self, mock_blob):
        # Configure mock to simulate network failure
        mock_blob.open.side_effect = TransientError("Network connection lost")

        # Test that the endpoint handles the network failure appropriately
        with self.assertRaises(HTTPException) as context:
            chapter_loader(self.test_request)
        
        # Verify error response
        self.assertEqual(context.exception.status_code, 404)
        self.assertTrue("TransientError" in str(context.exception.detail))