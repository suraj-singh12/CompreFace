# Face Recognition System (CompreFace + Custom Backend)

A minimal, production-oriented face recognition system built on top of **CompreFace** with a custom backend for metadata management.

---

## 🧱 Architecture

```
Image
  ↓
Custom Backend (FastAPI)
  ↓
CompreFace API
  ↓
Face Recognition + Age/Gender
  ↓
Custom DB (JSON)
  ↓
Enriched Response
```

### Responsibilities

* **CompreFace** → Face detection, recognition, age, gender
* **Backend** → Business logic, identity mapping, metadata
* **DB (JSON)** → Stores additional user details

---

## ⚙️ Setup

### 1. Install dependencies

```bash
conda create -n facerec python=3.10 -y
conda activate facerec

pip install fastapi uvicorn requests python-multipart
```

---

### 2. Start CompreFace

```bash
cd CompreFace
docker compose up -d
```

Check:

```
http://localhost:8000
```

---

### 3. Configure backend

Edit `backend/config.py`:

```python
API_URL = "http://localhost:8000/api/v1/recognition"
API_KEY = "YOUR_API_KEY"

DB_PATH = "../data/db.json"
THRESHOLD = 0.75
```

---

### 4. Run backend

```bash
cd facerec-system/backend
uvicorn app:app --reload --port 8001
```

---

### 5. Access APIs

* Backend Docs → [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
* CompreFace UI → [http://localhost:8000](http://localhost:8000)

---

## 🚀 API Endpoints

### 🔍 `/recognize`

* Input: Image
* Output:

  * Recognized person (if match)
  * Age & gender (from CompreFace)
  * Additional details (from DB)

---

### ➕ `/register`

* Input:

  * Image
  * Name
  * Additional details

* Behavior:

  * Checks if person already exists
  * If yes → adds image to existing subject
  * If no → creates new subject

---

## 🧠 Core Logic

### Recognition Flow

```
Image → CompreFace → subject_id
                  ↓
             DB lookup
                  ↓
        return enriched result
```

---

### Registration Flow

```
Image → Recognize
  ↓
If match → append image
If no match → create subject
  ↓
Store metadata in DB
```

---

## ⚠️ Notes

* Age & gender are **predicted**, not stored
* Metadata is **external to CompreFace**
* Do not modify CompreFace backend for custom fields
* Use multiple images per user for better accuracy

---

## 🪖 Run Commands (Quick Start)

```bash
# Start Docker
open -a Docker

# Start CompreFace
cd CompreFace
docker compose up -d

# Activate env
conda activate facerec

# Run backend
cd facerec-system/backend
uvicorn app:app --reload --port 8001
```

---

## 🧠 Design Principle

> CompreFace handles vision.
> Backend handles identity.


---
