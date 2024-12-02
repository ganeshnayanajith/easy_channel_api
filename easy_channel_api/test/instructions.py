import requests

url = "http://localhost:5000/instructions"

payload = "{\r\n    \"input\":\"Eye Trauma\"\r\n}"
headers = {
    'Authorization': 'Bearer ',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
