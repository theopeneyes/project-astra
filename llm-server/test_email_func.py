
# # import requests
# payload  = {
#      "request_key": "OpenEyes_1224EzZykXxo",
#      "email_key": "RequestComplated",
#      "request_emails": [
#           "test1.openeyes@gmail.com"
#      ],
#      "dynamic_data": {
#           "current_year": "2025"
#      }
# }

# # response = requests.post("https://oeservices.uatbyopeneyes.com/api/v1/sendMailWithOpenEyesMT", json=payload)
# # print(response)



# import requests

# url = "http://127.0.0.1:8000/send-email"
# data = {"key": "value"}
# response = requests.post(url, json={"email":"openeyesvo@gmail.com"})
# print(response)
import requests 
payload = {
    "filename": "lbdl",
    "email_id": "pratyush.rao.ai@gmail.com",
    "number_of_pages": 5,
    "language_code": "en"
}
response = requests.post("http://127.0.0.1:8000/extract_contents_page", json=payload)
print(response)