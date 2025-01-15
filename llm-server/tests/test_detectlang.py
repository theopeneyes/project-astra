# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import Mock, patch, mock_open
# import json
# import base64
# import sys
# import os
# from pathlib import Path

# # Add the project root to Python path
# project_root = Path(__file__).parent.parent
# sys.path.append(str(project_root))

# # Import your FastAPI app and models
# from main import app
# from models import RequestModel, DetectedLanguageResponseModel

# client = TestClient(app)

# @pytest.fixture
# def mock_bucket():
#     with patch('main.bucket') as mock:
#         yield mock

# @pytest.fixture
# def sample_image_data():
#     sample_text = "Hello! ∑≠π★☺ 你好 λα"
#     return base64.b64encode(sample_text.encode()).decode()

# @pytest.fixture
# def mock_detect_language():
#     with patch('main.detect_language') as mock:
#         mock.return_value = (0.95, "English", 150)
#         yield mock

# @pytest.mark.asyncio
# async def test_detect_lang_with_special_chars(mock_bucket, mock_detect_language):
#     # Mock data
#     test_filename = "test_doc.pdf"
#     test_email = "test@example.com"
    
#     # Create mock image blob with proper context manager mocking
#     mock_blob = Mock()
#     mock_images = [
#         {"img_b64": "base64_encoded_image_data"}
#     ]
    
#     # Mock the file content
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob

#     # Test request
#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     # Assertions
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["detected_language"] == "english"
#     assert response_data["email_id"] == test_email
#     assert response_data["filename"] == test_filename
#     assert "confidence" in response_data
#     assert "time" in response_data
#     assert "token_count" in response_data

# @pytest.mark.asyncio
# async def test_detect_lang_file_not_found(mock_bucket):
#     # Setup mock to raise exception
#     mock_blob = Mock()
#     mock_blob.open.side_effect = FileNotFoundError("File not found")
#     mock_bucket.blob.return_value = mock_blob

#     # Test request
#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": "nonexistent.pdf",
#             "email_id": "test@example.com"
#         }
#     )

#     # Assertions
#     assert response.status_code == 404
#     assert "Error" in response.json()["detail"]

# @pytest.mark.asyncio
# async def test_detect_lang_special_characters(mock_bucket, mock_detect_language, sample_image_data):
#     test_filename = "special_chars.pdf"
#     test_email = "test@example.com"
    
#     # Create mock image blob with special characters and proper context manager mocking
#     mock_blob = Mock()
#     mock_images = [
#         {"img_b64": sample_image_data}
#     ]
    
#     # Mock the file content
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob

#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     assert response.status_code == 200
#     assert response.json()["detected_language"] == "english"



##########################################################



import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, mock_open
import json
import base64
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from main import app
from models import RequestModel, DetectedLanguageResponseModel

client = TestClient(app)

@pytest.fixture
def mock_bucket():
    with patch('main.bucket') as mock:
        yield mock

@pytest.fixture
def mock_detect_language():
    with patch('main.detect_language') as mock:
        # Default return value, will be overridden in specific tests
        mock.return_value = (0.95, "English", 150)
        yield mock

@pytest.fixture
def low_resource_samples():
    return {
        "dzongkha": {  # Bhutanese language
            "text": "ང་བཅས་ཀྱི་རྒྱལ་ཁབ་འདི་དགའ་སྐྱིད་ཀྱི་ཡུལ་ཨིན།",
            "confidence": 0.65
        },
        "hawaiian": {
            "text": "E hele mai i kaʻu papa ʻōlelo Hawaiʻi",
            "confidence": 0.70
        },
        "sami": {  # Northern Sami
            "text": "Buorre beaivi. Mo don leat odne?",
            "confidence": 0.60
        },
        "quechua": {
            "text": "Allillanchu. Imaynalla kashanki?",
            "confidence": 0.68
        }
    }

@pytest.mark.asyncio
@pytest.mark.parametrize("language", ["dzongkha", "hawaiian", "sami", "quechua"])
async def test_detect_low_resource_languages(mock_bucket, mock_detect_language, low_resource_samples, language):
    # Test data setup
    test_filename = f"{language}_sample.pdf"
    test_email = "test@example.com"
    sample_text = low_resource_samples[language]["text"]
    expected_confidence = low_resource_samples[language]["confidence"]
    
    # Encode the sample text
    encoded_text = base64.b64encode(sample_text.encode()).decode()
    
    # Create mock image blob
    mock_blob = Mock()
    mock_images = [
        {"img_b64": encoded_text}
    ]
    
    # Mock the file content
    mock_file = mock_open(read_data=json.dumps(mock_images))
    mock_blob.open = mock_file
    mock_bucket.blob.return_value = mock_blob
    
    # Set up mock detect_language to return appropriate values for this language
    mock_detect_language.return_value = (
        expected_confidence,
        language,
        len(sample_text.split())  # Approximate token count
    )

    # Test request
    response = client.post(
        "/detect_lang",
        json={
            "filename": test_filename,
            "email_id": test_email
        }
    )

    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    
    # Basic response structure checks
    assert response_data["filename"] == test_filename
    assert response_data["email_id"] == test_email
    assert "time" in response_data
    
    # Language-specific checks
    assert response_data["detected_language"] == language
    assert response_data["confidence"] <= 0.75  # Low-resource languages typically have lower confidence
    assert response_data["confidence"] >= 0.5   # But should still be above random chance

@pytest.mark.asyncio
async def test_mixed_low_resource_language(mock_bucket, mock_detect_language, low_resource_samples):
    """Test detection when a page contains mix of low-resource language and English"""
    test_filename = "mixed_language.pdf"
    test_email = "test@example.com"
    
    # Mix Quechua and English
    mixed_text = f"{low_resource_samples['quechua']['text']} This is some English text."
    encoded_text = base64.b64encode(mixed_text.encode()).decode()
    
    # Create mock image blob
    mock_blob = Mock()
    mock_images = [
        {"img_b64": encoded_text}
    ]
    
    # Mock the file content
    mock_file = mock_open(read_data=json.dumps(mock_images))
    mock_blob.open = mock_file
    mock_bucket.blob.return_value = mock_blob
    
    # Mock detection to return lower confidence due to mixed languages
    mock_detect_language.return_value = (0.55, "quechua", len(mixed_text.split()))

    # Test request
    response = client.post(
        "/detect_lang",
        json={
            "filename": test_filename,
            "email_id": test_email
        }
    )

    # Assertions
    assert response.status_code == 200
    response_data = response.json()
    assert "confidence" in response_data
    assert response_data["confidence"] < 0.7  # Lower confidence expected for mixed language content