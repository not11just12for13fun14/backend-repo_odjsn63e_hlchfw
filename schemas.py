"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

# ---------------------------------------------------------------------------
# Core domain schemas for Child Immunization Registration System
# Each class name (lowercase) maps to a MongoDB collection name
# ---------------------------------------------------------------------------

class Guardian(BaseModel):
    """
    Guardians collection schema
    Collection: "guardian"
    """
    name: str = Field(..., description="Guardian full name")
    phone: Optional[str] = Field(None, description="Contact phone number")
    email: Optional[str] = Field(None, description="Email address")
    relationship: Optional[str] = Field(None, description="Relationship to child (mother, father, etc.)")
    address: Optional[str] = Field(None, description="Home address")

class Child(BaseModel):
    """
    Children collection schema
    Collection: "child"
    """
    first_name: str = Field(..., description="Child first name")
    last_name: str = Field(..., description="Child last name")
    gender: Optional[str] = Field(None, description="Gender")
    date_of_birth: date = Field(..., description="Date of birth")
    birth_certificate_number: Optional[str] = Field(None, description="Birth certificate number")
    national_id: Optional[str] = Field(None, description="National ID / Reg no")
    guardian_id: Optional[str] = Field(None, description="Reference to guardian document ID")

class Vaccine(BaseModel):
    """
    Vaccines collection schema
    Collection: "vaccine"
    """
    name: str = Field(..., description="Vaccine name (e.g., BCG, HepB, DTP)")
    code: Optional[str] = Field(None, description="Program code")
    manufacturer: Optional[str] = Field(None, description="Manufacturer")
    doses_required: Optional[int] = Field(1, ge=1, description="Number of doses required in schedule")
    recommended_ages_weeks: Optional[List[int]] = Field(None, description="Recommended ages in weeks for doses")

class Immunization(BaseModel):
    """
    Immunization records schema
    Collection: "immunization"
    """
    child_id: str = Field(..., description="Reference to child document ID")
    vaccine_id: str = Field(..., description="Reference to vaccine document ID")
    dose_number: int = Field(..., ge=1, description="Dose sequence number")
    date_administered: date = Field(..., description="Date dose administered")
    administered_by: Optional[str] = Field(None, description="Healthcare worker name")
    location: Optional[str] = Field(None, description="Facility/Location")
    lot_number: Optional[str] = Field(None, description="Vaccine lot/batch number")
    adverse_events: Optional[str] = Field(None, description="Any reported adverse events")

class Appointment(BaseModel):
    """
    Scheduled vaccination appointments
    Collection: "appointment"
    """
    child_id: str = Field(..., description="Reference to child document ID")
    vaccine_id: str = Field(..., description="Reference to vaccine document ID")
    dose_number: int = Field(..., ge=1, description="Dose to be administered")
    scheduled_date: date = Field(..., description="Scheduled appointment date")
    notes: Optional[str] = Field(None, description="Notes for appointment")

# Legacy example schemas kept for reference (not used by the app):

class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")
