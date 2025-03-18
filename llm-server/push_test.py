import requests
import time

# Define the endpoint URL
url = "http://127.0.0.1:8000/generate_excel"  # Adjust the URL as needed

# Define the request payload
payload = {
    "email_id": "pratyush.rao.ai@gmail.com",
    "filename": "lbdl.pdf"
}

# Measure the time taken for the request
start_time = time.time()
response = requests.post(url, json=payload)
end_time = time.time()

# Calculate the duration
duration = end_time - start_time

# Print the results
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")
print(f"Time Taken: {duration:.2f} seconds")
