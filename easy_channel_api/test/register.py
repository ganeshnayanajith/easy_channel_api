import requests

url = "http://localhost:5000/register"

payload = "{\r\n    \"email\": \"ganeshnayanajith40@gmail.com\",\r\n    \"first_name\": \"ganesh\",\r\n    \"last_name\": \"nayanajith\",\r\n    \"password\": \"\"\r\n}"
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
