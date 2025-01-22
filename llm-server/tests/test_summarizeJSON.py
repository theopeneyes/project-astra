# import pytest
# from unittest.mock import Mock, patch
# from google.cloud import storage
# from fastapi import HTTPException
# from models import RewriteJSONRequestModel
# from main import rewrite_json

# @pytest.fixture
# def mock_blob():
#     blob = Mock(spec=storage.Blob)
#     # Set blob size to 11MB (exceeding 10MB limit)
#     blob.size = 11 * 1024 * 1024
#     return blob

# @pytest.mark.asyncio
# async def test_file_size_limit(mock_blob):
#     request = RewriteJSONRequestModel(
#         email_id="test@example.com",
#         filename="test.pdf",
#         chapter_name="chapter1",
#         node_id=1,
#         language_code="en"
#     )
    
#     with pytest.raises(HTTPException) as exc_info:
#         with patch('main.bucket.blob', return_value=mock_blob):
#             await rewrite_json(request)
    
#     assert exc_info.value.status_code == 413
#     assert "Error :ValueError" in exc_info.value.detail



################################################################################################################################################################




import pytest
from unittest.mock import Mock, patch
from google.cloud import storage
from fastapi import HTTPException
from models import RewriteJSONRequestModel
from main import rewrite_json

@pytest.fixture
def mock_blob():
    blob = Mock(spec=storage.Blob)
    # Default size for mock blobs (5MB for most tests)
    blob.size = 5 * 1024 * 1024
    return blob

@pytest.mark.asyncio
async def test_file_size_limit(mock_blob):
    mock_blob.size = 11 * 1024 * 1024  # 11MB to exceed the limit

    request = RewriteJSONRequestModel(
        email_id="test@example.com",
        filename="test.json",
        chapter_name="chapter1",
        node_id=1,
        language_code="en"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        with patch('main.bucket.blob', return_value=mock_blob):
            await rewrite_json(request)
    
    # Check if the error message contains the expected "File is bigger than 10 Mb." detail
    assert exc_info.value.status_code == 413  # HTTP 413 Payload Too Large
    assert "File is bigger than 10 Mb." in exc_info.value.detail

@pytest.mark.asyncio
async def test_unsupported_file_format(mock_blob):
    request = RewriteJSONRequestModel(
        email_id="test@example.com",
        filename="test.pdf",  # Unsupported format
        chapter_name="chapter1",
        node_id=1,
        language_code="en"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        with patch('main.bucket.blob', return_value=mock_blob):
            await rewrite_json(request)
    
    # Check if the error message contains the expected "Unsupported File Format" detail
    assert exc_info.value.status_code == 415  # HTTP 415 Unsupported Media Type
    assert "Unsupported File Format" in exc_info.value.detail