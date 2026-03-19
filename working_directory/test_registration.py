import requests

API_KEY = "b43b0f25-9b72-48ac-b22a-9b7f801fc31b"
IMAGE_PATH = "test.jpg"
SUBJECT = "user_1"

url = "http://localhost:8000/api/v1/recognition/faces"

with open(IMAGE_PATH, "rb") as f:
    response = requests.post(
        url,
        headers={"x-api-key": API_KEY},
        files={
            "file": f,
            "subject": (None, SUBJECT)
        }
    )

print(response.json())
