from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File, Form, FastAPI
import requests
import json
import time
from config import API_URL, API_KEY, DB_PATH, THRESHOLD

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
#    allow_origins=["*"],  # for dev only
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- DB --------
def load_db():
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)

# -------- ROUTES --------

@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    db = load_db()
    
    image_bytes = await file.read()
        
    res = requests.post(
        f"{API_URL}/recognize",
        headers={"x-api-key": API_KEY},
        files={"file": ("image.jpg", image_bytes, "image/jpeg")},
        params={"face_plugins": "age,gender"}
    ).json()
    
    if not res.get("result"):
        return {"status": "no_face"}
        
    face = res["result"][0]
    subjects = face.get("subjects", [])

    # -------- CompreFace predicted --------
    gender_data = face.get("gender", {})
    age_data = face.get("age", {})
        
    computed_gender = gender_data.get("value")
     
    age = None
    if "low" in age_data and "high" in age_data:
        age = (age_data["low"] + age_data["high"]) // 2

    if subjects and subjects[0]["similarity"] > THRESHOLD:
        sid = subjects[0]["subject"]
        addl_info = db.get(sid, {})

        # -------- Gender selection logic --------
        saved_gender = addl_info.get("gender")

        if saved_gender:
            final_gender = f"{saved_gender} (saved)"
        elif computed_gender:
            final_gender = f"{computed_gender} (computed)"
        else:
            final_gender = None

        return {
            "status": "recognized",
            "subject_id": sid,
            "similarity": subjects[0]["similarity"],
            "name": addl_info.get("name"),
            "age": age,
            "gender": final_gender,
            "comments": addl_info.get("comments")
        }
    
    return {
        "status": "unknown",
        "age": age,
        "gender": computed_gender
    }


@app.post("/register")
async def register(
    file: UploadFile = File(...),
    name: str = Form(...),
    gender: str = Form(""),
    comments: str = Form(""),
):
    db = load_db()
    image_bytes = await file.read()

    # Step 1: Recognize face
    res = requests.post(
        f"{API_URL}/recognize",
        headers={"x-api-key": API_KEY},
        files={"file": ("image.jpg", image_bytes, "image/jpeg")}
    ).json()

    if res.get("result"):
        face = res["result"][0]
        subjects = face.get("subjects", [])

        if subjects and subjects[0]["similarity"] > THRESHOLD:
            sid = subjects[0]["subject"]
            similarity = subjects[0]["similarity"]

            # 🪖 Case 1: Existing user in DB
            if sid in db:

                # duplicate image check
                if similarity > 0.98:
                    return {
                        "status": "duplicate_image",
                        "subject_id": sid,
                        "name": db[sid].get("name")
                    }

                # add image
                requests.post(
                    f"{API_URL}/faces",
                    headers={"x-api-key": API_KEY},
                    files={
                        "file": ("image.jpg", image_bytes, "image/jpeg"),
                        "subject": (None, sid)
                    }
                )

                return {
                    "status": "image_added_existing_user",
                    "subject_id": sid,
                    "name": db[sid].get("name")
                }

            # 🪖 Case 2: Exists in CompreFace but not in DB
            db[sid] = {
                "name": name,
                "comments": comments,
                "gender": gender if gender else None
            }
            save_db(db)

            return {
                "status": "metadata_added_existing_face",
                "subject_id": sid,
                "name": name
            }

    # 🪖 Case 3: New user
    subject_id = f"user_{int(time.time())}"

    reg_res = requests.post(
        f"{API_URL}/faces",
        headers={"x-api-key": API_KEY},
        files={
            "file": ("image.jpg", image_bytes, "image/jpeg"),
            "subject": (None, subject_id)
        }
    ).json()

    if "image_id" not in reg_res:
        return {
            "status": "registration_failed",
            "error": reg_res
        }

    db[subject_id] = {
        "name": name,
        "comments": comments,
        "gender": gender if gender else None
    }
    save_db(db)

    return {
        "status": "registered_new_user",
        "subject_id": subject_id,
        "name": name
    }
