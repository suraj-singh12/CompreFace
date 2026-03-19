import requests

API_URL = "http://localhost:8000/api/v1/recognition/recognize"
API_KEY = "b43b0f25-9b72-48ac-b22a-9b7f801fc31b"

IMAGE_PATH = "test2.jpg"  # keep any face image here

with open(IMAGE_PATH, "rb") as f:
    response = requests.post(
        API_URL,
        headers={"x-api-key": API_KEY},
        files={"file": f}
    )

print(response.json())
