"""Root of the microservice"""

from fastapi import FastAPI, Path, HTTPException, Query

from utils import valid_fields
from db import (
    get_all_patients,
    get_patient_by_id,
    get_patients_by_name,
    sort_records_by_param,
)

app = FastAPI()


# Route handlers


@app.get("/")
def index():
    return {"message": "Patient Management System 🏥"}


@app.get("/about")
def about():
    return {"message": "This is a microservice for managing patient records."}


@app.get("/view")
def view():
    data: list[dict] | None = get_all_patients()

    if data is None:
        raise HTTPException(status_code=500, detail="Failed to fetch patient records.")

    if data == []:
        return {"message": "No patient records found."}

    return list(data)


@app.get("/patient/id/{patient_id}")
def view_patient_by_id(
    patient_id: str = Path(
        ..., description="Patient ID in the database.", example="P001"
    )
):
    data: dict | None = get_patient_by_id(patient_id)

    if data is None:
        raise HTTPException(status_code=500, detail="Failed to fetch patient record.")

    if data == {}:
        raise HTTPException(
            status_code=404, detail=f"Patient with ID : '{patient_id}' not found."
        )

    return data


@app.get("/patient/")
def view_patients_by_name(
    patient_name: str = Query(
        ..., description="Patient name in the database.", example="John Doe"
    )
):
    data: list[dict] | None = get_patients_by_name(patient_name)

    if data is None:
        raise HTTPException(
            status_code=500, detail="Failed to fetch patient record(s)."
        )

    if data == []:
        raise HTTPException(
            status_code=404,
            detail=f"Patient(s) with name : '{patient_name}' not found.",
        )

    return data


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,
        description="Sort records on the basis of height, weight or bmi.",
    ),
    order: str = Query("asc", description="Sort in ascending or descending order."),
):
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sorting field. Select from {', '.join(valid_fields)}.",
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sorting order. Select either 'asc' or 'desc'.",
        )

    data: list[dict] | None = sort_records_by_param(
        sort_by, True if order == "desc" else False
    )

    if data is None:
        raise HTTPException(status_code=500, detail="Failed to fetch patient records.")

    if data == []:
        return {"message": "No patient records found."}

    return data
