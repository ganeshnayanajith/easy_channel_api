import requests

url = "http://localhost:5000"

payload = "{\r\n    \"input\":\"sneezing\"\r\n}"
headers = {
    'Authorization': 'Bearer ',
    'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
