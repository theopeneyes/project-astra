import time
import json 

def get_rate_limit_metadata(email_id: str, bucket, windows_seconds: int):
    """Fetch rate-limiting metadata for a specific user from GCP bucket."""
    blob_name = f"rate_limit/{email_id}.json"
    blob = bucket.blob(blob_name)

    if blob.exists():
        rate_limit_data = json.loads(blob.download_as_text())
    else:
        rate_limit_data = {"count": 0, "reset_time": time.time() + windows_seconds}

    return blob, rate_limit_data

def update_rate_limit_metadata(blob, rate_limit_data):
    """Update rate-limiting metadata in GCP bucket."""
    blob.upload_from_string(json.dumps(rate_limit_data), content_type="application/json")