# Face Recognition System

A local face recognition system with a clean interface.
Designed for reliable identification and controlled user registration.

---

## 🚀 Capabilities

* Recognizes faces from images
* Displays name, age, gender, comments
* Registers new individuals
* Prevents duplicate identities
* Improves accuracy with additional images

---

## ⚙️ Requirements

* Python 3.10+
* Conda (recommended)
* Docker (for CompreFace)

---

## 🪖 Setup

```bash
# Start CompreFace
cd CompreFace
docker compose up -d
```

Access: http://localhost:8000
Create a recognition service and obtain the API key.

---

```bash
# Backend setup
conda create -n facerec python=3.10 -y
conda activate facerec

pip install fastapi uvicorn requests python-multipart
```

Update `config.py` with the API key.

---

## ▶️ Run

```bash
# Start backend
cd backend
uvicorn app:app --reload --port 8001

# Start UI
cd ui
python3 -m http.server 3000
```

Access: http://localhost:3000

---

## 👤 Usage

1. Upload an image
2. Select **Recognize**

* If identified → system displays stored details
* If not identified → enter details and **Register**

---

Precise. Controlled. Extendable.
