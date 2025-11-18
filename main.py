import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from database import create_document, get_documents, db
from schemas import Child, Guardian, Vaccine, Immunization, Appointment

app = FastAPI(title="Child Immunization Registry API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Child Immunization Registry API"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# ---------------------------------------------------------------------------
# Request models for creation endpoints
# ---------------------------------------------------------------------------

class CreateGuardianRequest(Guardian):
    pass

class CreateChildRequest(Child):
    pass

class CreateVaccineRequest(Vaccine):
    pass

class CreateImmunizationRequest(Immunization):
    pass

class CreateAppointmentRequest(Appointment):
    pass

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def ensure_db():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/guardians")
def create_guardian(payload: CreateGuardianRequest):
    ensure_db()
    guardian_id = create_document("guardian", payload)
    return {"id": guardian_id}

@app.get("/api/guardians")
def list_guardians():
    ensure_db()
    docs = get_documents("guardian")
    # Convert ObjectId to string
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.post("/api/children")
def create_child(payload: CreateChildRequest):
    ensure_db()
    child_id = create_document("child", payload)
    return {"id": child_id}

@app.get("/api/children")
def list_children():
    ensure_db()
    docs = get_documents("child")
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.post("/api/vaccines")
def create_vaccine(payload: CreateVaccineRequest):
    ensure_db()
    vaccine_id = create_document("vaccine", payload)
    return {"id": vaccine_id}

@app.get("/api/vaccines")
def list_vaccines():
    ensure_db()
    docs = get_documents("vaccine")
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.post("/api/immunizations")
def create_immunization(payload: CreateImmunizationRequest):
    ensure_db()
    immu_id = create_document("immunization", payload)
    return {"id": immu_id}

@app.get("/api/immunizations")
def list_immunizations(child_id: Optional[str] = None):
    ensure_db()
    filter_q = {"child_id": child_id} if child_id else None
    docs = get_documents("immunization", filter_q)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.post("/api/appointments")
def create_appointment(payload: CreateAppointmentRequest):
    ensure_db()
    appt_id = create_document("appointment", payload)
    return {"id": appt_id}

@app.get("/api/appointments")
def list_appointments(child_id: Optional[str] = None):
    ensure_db()
    filter_q = {"child_id": child_id} if child_id else None
    docs = get_documents("appointment", filter_q)
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
