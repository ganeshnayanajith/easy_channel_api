import requests

url = "http://localhost:5000/specializations"

payload = "{\r\n    \"input\":\"i have itching and skin rash dischromic patches. i want to know the doctor specialization\"\r\n}"
headers = {
    'Authorization': 'Bearer ',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
