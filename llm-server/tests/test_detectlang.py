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

# from main import app
# from models import RequestModel, DetectedLanguageResponseModel

# client = TestClient(app)

# @pytest.fixture
# def mock_bucket():
#     with patch('main.bucket') as mock:
#         yield mock

# @pytest.fixture
# def mock_detect_language():
#     with patch('main.detect_language') as mock:
#         # Default return value, will be overridden in specific tests
#         mock.return_value = (0.95, "English", 150)
#         yield mock

# @pytest.fixture
# def low_resource_samples():
#     return {
#         "dzongkha": {  # Bhutanese language
#             "text": "ང་བཅས་ཀྱི་རྒྱལ་ཁབ་འདི་དགའ་སྐྱིད་ཀྱི་ཡུལ་ཨིན།",
#             "confidence": 0.65
#         },
#         "hawaiian": {
#             "text": "E hele mai i kaʻu papa ʻōlelo Hawaiʻi",
#             "confidence": 0.70
#         },
#         "sami": {  # Northern Sami
#             "text": "Buorre beaivi. Mo don leat odne?",
#             "confidence": 0.60
#         },
#         "quechua": {
#             "text": "Allillanchu. Imaynalla kashanki?",
#             "confidence": 0.68
#         }
#     }

# @pytest.mark.asyncio
# @pytest.mark.parametrize("language", ["dzongkha", "hawaiian", "sami", "quechua"])
# async def test_detect_low_resource_languages(mock_bucket, mock_detect_language, low_resource_samples, language):
#     # Test data setup
#     test_filename = f"{language}_sample.pdf"
#     test_email = "test@example.com"
#     sample_text = low_resource_samples[language]["text"]
#     expected_confidence = low_resource_samples[language]["confidence"]
    
#     # Encode the sample text
#     encoded_text = base64.b64encode(sample_text.encode()).decode()
    
#     # Create mock image blob
#     mock_blob = Mock()
#     mock_images = [
#         {"img_b64": encoded_text}
#     ]
    
#     # Mock the file content
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Set up mock detect_language to return appropriate values for this language
#     mock_detect_language.return_value = (
#         expected_confidence,
#         language,
#         len(sample_text.split())  # Approximate token count
#     )

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
    
#     # Basic response structure checks
#     assert response_data["filename"] == test_filename
#     assert response_data["email_id"] == test_email
#     assert "time" in response_data
    
#     # Language-specific checks
#     assert response_data["detected_language"] == language
#     assert response_data["confidence"] <= 0.75  # Low-resource languages typically have lower confidence
#     assert response_data["confidence"] >= 0.5   # But should still be above random chance

# @pytest.mark.asyncio
# async def test_mixed_low_resource_language(mock_bucket, mock_detect_language, low_resource_samples):
#     """Test detection when a page contains mix of low-resource language and English"""
#     test_filename = "mixed_language.pdf"
#     test_email = "test@example.com"
    
#     # Mix Quechua and English
#     mixed_text = f"{low_resource_samples['quechua']['text']} This is some English text."
#     encoded_text = base64.b64encode(mixed_text.encode()).decode()
    
#     # Create mock image blob
#     mock_blob = Mock()
#     mock_images = [
#         {"img_b64": encoded_text}
#     ]
    
#     # Mock the file content
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Mock detection to return lower confidence due to mixed languages
#     mock_detect_language.return_value = (0.55, "quechua", len(mixed_text.split()))

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
#     assert "confidence" in response_data
#     assert response_data["confidence"] < 0.7  # Lower confidence expected for mixed language content




######  Tests for image detection  ######



# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import Mock, patch, mock_open
# import json
# import base64
# import sys
# from pathlib import Path

# # Add the project root to Python path
# project_root = Path(__file__).parent.parent
# sys.path.append(str(project_root))

# from main import app
# from models import RequestModel, DetectedLanguageResponseModel

# client = TestClient(app)

# @pytest.fixture
# def mock_bucket():
#     with patch('main.bucket') as mock:
#         yield mock

# @pytest.fixture
# def mock_detect_language():
#     with patch('main.detect_language') as mock:
#         mock.return_value = (0.95, "English", 150)
#         yield mock

# @pytest.fixture
# def sample_images():
#     return {
#         "only_image": {
#             "img_b64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",  # 1x1 transparent PNG
#             "expected_confidence": 0.1,
#             "expected_language": "unknown"
#         },
#         "text_with_small_image": {
#             "text": "This is a sample English text",
#             "img_b64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
#             "expected_confidence": 0.85,
#             "expected_language": "english"
#         },
#         "text_with_large_image": {
#             "text": "Sample text with large image",
#             "img_b64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
#             "expected_confidence": 0.75,
#             "expected_language": "english"
#         }
#     }

# @pytest.mark.asyncio
# async def test_page_with_only_image(mock_bucket, mock_detect_language, sample_images):
#     """Test language detection on a page that contains only an image"""
#     test_filename = "image_only.pdf"
#     test_email = "test@example.com"
    
#     # Create mock image blob
#     mock_blob = Mock()
#     mock_images = [
#         {"img_b64": sample_images["only_image"]["img_b64"]}
#     ]
    
#     # Mock the file content
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Set expected low confidence for image-only content
#     mock_detect_language.return_value = (
#         sample_images["only_image"]["expected_confidence"],
#         sample_images["only_image"]["expected_language"],
#         0
#     )

#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["confidence"] < 0.2  # Very low confidence for image-only content
#     assert response_data["detected_language"] == "unknown"

# @pytest.mark.asyncio
# async def test_page_with_text_and_small_image(mock_bucket, mock_detect_language, sample_images):
#     """Test language detection on a page with text and a small image"""
#     test_filename = "text_with_small_image.pdf"
#     test_email = "test@example.com"
    
#     # Combine text and image data
#     mock_blob = Mock()
#     mock_images = [
#         {
#             "img_b64": base64.b64encode(
#                 sample_images["text_with_small_image"]["text"].encode()
#             ).decode()
#         },
#         {
#             "img_b64": sample_images["text_with_small_image"]["img_b64"]
#         }
#     ]
    
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Set expected high confidence for text with small image
#     mock_detect_language.return_value = (
#         sample_images["text_with_small_image"]["expected_confidence"],
#         sample_images["text_with_small_image"]["expected_language"],
#         len(sample_images["text_with_small_image"]["text"].split())
#     )

#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["confidence"] > 0.8  # High confidence as text is clear
#     assert response_data["detected_language"] == "english"

# @pytest.mark.asyncio
# async def test_page_with_multiple_images(mock_bucket, mock_detect_language, sample_images):
#     """Test language detection on a page with multiple images and text"""
#     test_filename = "multiple_images.pdf"
#     test_email = "test@example.com"
    
#     mock_blob = Mock()
#     # Create a page with multiple images and some text
#     mock_images = [
#         {"img_b64": sample_images["text_with_large_image"]["img_b64"]},
#         {
#             "img_b64": base64.b64encode(
#                 sample_images["text_with_large_image"]["text"].encode()
#             ).decode()
#         },
#         {"img_b64": sample_images["text_with_large_image"]["img_b64"]}
#     ]
    
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Set slightly lower confidence due to multiple images
#     mock_detect_language.return_value = (
#         sample_images["text_with_large_image"]["expected_confidence"],
#         sample_images["text_with_large_image"]["expected_language"],
#         len(sample_images["text_with_large_image"]["text"].split())
#     )

#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["confidence"] > 0.6  # Moderate confidence due to multiple images
#     assert response_data["detected_language"] == "english"
    
# @pytest.mark.asyncio
# async def test_image_heavy_multilingual_page(mock_bucket, mock_detect_language):
#     """Test language detection on a page with multiple images and multilingual text"""
#     test_filename = "image_heavy_multilingual.pdf"
#     test_email = "test@example.com"
    
#     mock_blob = Mock()
#     # Create content with multiple images and multilingual text
#     mixed_text = "Hello World! こんにちは世界! Bonjour le monde!"
#     mock_images = [
#         {"img_b64": "base64_image_1"},  # Image
#         {
#             "img_b64": base64.b64encode(mixed_text.encode()).decode()
#         },
#         {"img_b64": "base64_image_2"}   # Another image
#     ]
    
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Set lower confidence due to mixed languages and images
#     mock_detect_language.return_value = (0.45, "mixed", len(mixed_text.split()))

#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["confidence"] < 0.5  # Low confidence due to mixed languages and images
#     assert "token_count" in response_data



#### tests for false positives and false negatives #### 

# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import Mock, patch, mock_open
# import json
# import base64
# import sys
# from pathlib import Path

# # Add the project root to Python path
# project_root = Path(__file__).parent.parent
# sys.path.append(str(project_root))

# from main import app
# from models import RequestModel, DetectedLanguageResponseModel

# client = TestClient(app)

# @pytest.fixture
# def mock_bucket():
#     with patch('main.bucket') as mock:
#         yield mock

# @pytest.fixture
# def mock_detect_language():
#     with patch('main.detect_language') as mock:
#         mock.return_value = (0.95, "English", 150)
#         yield mock

# @pytest.fixture
# def edge_case_samples():
#     return {
#         "similar_languages": {
#             # Hindi written in Latin script that looks like Sanskrit
#             "text": "Namaste, kaise hain aap? Aap ka shubh naam kya hai?",
#             "actual_language": "hindi",
#             "likely_false_positive": "sanskrit",
#             "expected_confidence": 0.75
#         },
#         "transliterated_text": {
#             # Japanese written in romaji
#             "text": "Watashi wa nihongo o benkyou shiteimasu",
#             "actual_language": "japanese",
#             "likely_false_positive": "english",
#             "expected_confidence": 0.65
#         },
#         "mixed_scripts": {
#             # Mix of Cyrillic and Latin that might confuse detection
#             "text": "Hello мир! Как дела? Fine спасибо!",
#             "actual_language": "mixed",
#             "likely_false_positive": "russian",
#             "expected_confidence": 0.55
#         },
#         "false_negative_case": {
#             # Valid English text with technical terms that might not be detected
#             "text": "SELECT COUNT(*) FROM table_name WHERE column1 = 'value' GROUP BY column2;",
#             "actual_language": "english",
#             "likely_false_negative": "code",
#             "expected_confidence": 0.45
#         }
#     }

# @pytest.mark.asyncio
# async def test_similar_languages_false_positive(mock_bucket, mock_detect_language, edge_case_samples):
#     """Test case where similar languages might cause false positive detection"""
#     test_filename = "similar_languages.pdf"
#     test_email = "test@example.com"
    
#     sample = edge_case_samples["similar_languages"]
#     encoded_text = base64.b64encode(sample["text"].encode()).decode()
    
#     # Create mock image blob
#     mock_blob = Mock()
#     mock_images = [{"img_b64": encoded_text}]
    
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Simulate false positive detection
#     mock_detect_language.return_value = (
#         sample["expected_confidence"],
#         sample["likely_false_positive"],
#         len(sample["text"].split())
#     )

#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     # Check if confidence is appropriately lower for potentially incorrect detection
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["confidence"] < 0.8
#     assert response_data["detected_language"] == sample["likely_false_positive"]

# @pytest.mark.asyncio
# async def test_transliterated_text_detection(mock_bucket, mock_detect_language, edge_case_samples):
#     """Test case where transliterated text might cause confusion"""
#     test_filename = "transliterated.pdf"
#     test_email = "test@example.com"
    
#     sample = edge_case_samples["transliterated_text"]
#     encoded_text = base64.b64encode(sample["text"].encode()).decode()
    
#     mock_blob = Mock()
#     mock_images = [{"img_b64": encoded_text}]
    
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Simulate confusion with English due to Latin script
#     mock_detect_language.return_value = (
#         sample["expected_confidence"],
#         sample["likely_false_positive"],
#         len(sample["text"].split())
#     )

#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["confidence"] < 0.7  # Lower confidence expected for transliterated text
#     assert response_data["detected_language"] == sample["likely_false_positive"]

# @pytest.mark.asyncio
# async def test_false_negative_technical_content(mock_bucket, mock_detect_language, edge_case_samples):
#     """Test case where technical content might cause false negatives"""
#     test_filename = "technical_content.pdf"
#     test_email = "test@example.com"
    
#     sample = edge_case_samples["false_negative_case"]
#     encoded_text = base64.b64encode(sample["text"].encode()).decode()
    
#     mock_blob = Mock()
#     mock_images = [{"img_b64": encoded_text}]
    
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Simulate false negative by returning low confidence
#     mock_detect_language.return_value = (
#         sample["expected_confidence"],
#         sample["likely_false_negative"],
#         len(sample["text"].split())
#     )

#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["confidence"] < 0.5  # Very low confidence for technical content
#     assert response_data["detected_language"] != sample["actual_language"]

# @pytest.mark.asyncio
# async def test_mixed_script_confusion(mock_bucket, mock_detect_language, edge_case_samples):
#     """Test case where mixed scripts might confuse language detection"""
#     test_filename = "mixed_scripts.pdf"
#     test_email = "test@example.com"
    
#     sample = edge_case_samples["mixed_scripts"]
#     encoded_text = base64.b64encode(sample["text"].encode()).decode()
    
#     mock_blob = Mock()
#     mock_images = [{"img_b64": encoded_text}]
    
#     mock_file = mock_open(read_data=json.dumps(mock_images))
#     mock_blob.open = mock_file
#     mock_bucket.blob.return_value = mock_blob
    
#     # Simulate confusion with primary script language
#     mock_detect_language.return_value = (
#         sample["expected_confidence"],
#         sample["likely_false_positive"],
#         len(sample["text"].split())
#     )

#     response = client.post(
#         "/detect_lang",
#         json={
#             "filename": test_filename,
#             "email_id": test_email
#         }
#     )

#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["confidence"] < 0.6  # Lower confidence for mixed scripts
#     assert response_data["detected_language"] == sample["likely_false_positive"]



##### test library errors for NLLB ####


import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, mock_open
import json
import base64
import sys
from pathlib import Path
from transformers import AutoModelForSeq2SeqGeneration, AutoTokenizer
import torch

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
def mock_nllb_model():
    with patch('main.AutoModelForSeq2SeqGeneration.from_pretrained') as mock:
        yield mock

@pytest.fixture
def mock_nllb_tokenizer():
    with patch('main.AutoTokenizer.from_pretrained') as mock:
        yield mock

@pytest.mark.asyncio
async def test_nllb_model_load_failure(mock_bucket, mock_nllb_model, mock_nllb_tokenizer):
    """Test handling of NLLB model loading failure"""
    test_filename = "test.pdf"
    test_email = "test@example.com"
    
    # Mock file content
    mock_blob = Mock()
    mock_images = [{"img_b64": base64.b64encode("Sample text".encode()).decode()}]
    mock_file = mock_open(read_data=json.dumps(mock_images))
    mock_blob.open = mock_file
    mock_bucket.blob.return_value = mock_blob
    
    # Simulate model loading error
    mock_nllb_model.side_effect = OSError("Failed to load NLLB model weights")

    response = client.post(
        "/detect_lang",
        json={
            "filename": test_filename,
            "email_id": test_email
        }
    )

    assert response.status_code == 503  # Service Unavailable
    assert "Failed to load NLLB model" in response.json()["detail"]

@pytest.mark.asyncio
async def test_nllb_cuda_out_of_memory(mock_bucket, mock_nllb_model, mock_nllb_tokenizer):
    """Test handling of CUDA out of memory error during NLLB inference"""
    test_filename = "test.pdf"
    test_email = "test@example.com"
    
    mock_blob = Mock()
    mock_images = [{"img_b64": base64.b64encode("Sample text".encode()).decode()}]
    mock_file = mock_open(read_data=json.dumps(mock_images))
    mock_blob.open = mock_file
    mock_bucket.blob.return_value = mock_blob
    
    # Set up model to raise CUDA OOM error
    mock_model = Mock()
    mock_model.generate.side_effect = torch.cuda.OutOfMemoryError("CUDA out of memory")
    mock_nllb_model.return_value = mock_model

    response = client.post(
        "/detect_lang",
        json={
            "filename": test_filename,
            "email_id": test_email
        }
    )

    assert response.status_code == 503
    assert "CUDA out of memory" in response.json()["detail"]

@pytest.mark.asyncio
async def test_nllb_tokenizer_error(mock_bucket, mock_nllb_model, mock_nllb_tokenizer):
    """Test handling of NLLB tokenizer errors"""
    test_filename = "test.pdf"
    test_email = "test@example.com"
    
    mock_blob = Mock()
    mock_images = [{"img_b64": base64.b64encode("Sample text".encode()).decode()}]
    mock_file = mock_open(read_data=json.dumps(mock_images))
    mock_blob.open = mock_file
    mock_bucket.blob.return_value = mock_blob
    
    # Simulate tokenizer error
    mock_nllb_tokenizer.side_effect = ValueError("Invalid tokenizer configuration")

    response = client.post(
        "/detect_lang",
        json={
            "filename": test_filename,
            "email_id": test_email
        }
    )

    assert response.status_code == 503
    assert "Tokenizer error" in response.json()["detail"]

@pytest.mark.asyncio
async def test_nllb_model_timeout(mock_bucket, mock_nllb_model, mock_nllb_tokenizer):
    """Test handling of NLLB model timeout during inference"""
    test_filename = "test.pdf"
    test_email = "test@example.com"
    
    mock_blob = Mock()
    mock_images = [{"img_b64": base64.b64encode("Sample text".encode()).decode()}]
    mock_file = mock_open(read_data=json.dumps(mock_images))
    mock_blob.open = mock_file
    mock_bucket.blob.return_value = mock_blob
    
    # Simulate model timeout
    mock_model = Mock()
    mock_model.generate.side_effect = TimeoutError("Model inference timed out")
    mock_nllb_model.return_value = mock_model

    response = client.post(
        "/detect_lang",
        json={
            "filename": test_filename,
            "email_id": test_email
        }
    )

    assert response.status_code == 504  # Gateway Timeout
    assert "Model inference timed out" in response.json()["detail"]

@pytest.mark.asyncio
async def test_nllb_fallback_mechanism(mock_bucket, mock_nllb_model, mock_nllb_tokenizer):
    """Test fallback to backup language detection when NLLB fails"""
    test_filename = "test.pdf"
    test_email = "test@example.com"
    
    mock_blob = Mock()
    mock_images = [{"img_b64": base64.b64encode("Sample text".encode()).decode()}]
    mock_file = mock_open(read_data=json.dumps(mock_images))
    mock_blob.open = mock_file
    mock_bucket.blob.return_value = mock_blob
    
    # Simulate NLLB failure but successful fallback
    mock_nllb_model.side_effect = Exception("NLLB Failed")
    
    with patch('main.fallback_detect_language') as mock_fallback:
        mock_fallback.return_value = (0.7, "english", 50)
        
        response = client.post(
            "/detect_lang",
            json={
                "filename": test_filename,
                "email_id": test_email
            }
        )

        assert response.status_code == 200
        assert response.json()["detected_language"] == "english"
        assert response.json()["confidence"] == 0.7
        assert "fallback_method" in response.json()  # Indicating fallback was used