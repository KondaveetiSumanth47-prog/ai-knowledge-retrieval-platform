import requests

response = requests.post(
    "http://127.0.0.1:5000/ask",
    json={"question": "What is RAG?"}
)

print("Status Code:", response.status_code)
print("Response:")
print(response.text)