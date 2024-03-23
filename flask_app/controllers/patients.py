from flask import render_template, redirect, request, session, flash

from flask_app.models.patient import Patient
from flask_app.models.provider import Provider


from flask_app import app
from datetime import datetime


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/dashboard")
def show_all_patients():
    if "provider_id" not in session:
        return redirect("/")
    patients = Patient.get_all()
    print("this")
    return render_template("all_patients.html", patients=patients)

@app.route("/create")
def create():
    if "provider_id" not in session:
        return redirect("/")
    provider_id = session["provider_id"]
    return render_template("add_patient.html")

@app.route("/create", methods=["POST"])
def add_patient():
    if "provider_id" not in session:
        return redirect("/")
    provider_id = session["provider_id"]

    if not Patient.validate_patient(request.form):
        return redirect("/create")
    
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "age" : request.form["age"],
        "language" : request.form["language"],
        "gender": request.form["gender"],
        "insurance" : request.form["insurance"],
        "date_enrolled" : request.form["date_enrolled"],
        "medical_condition": request.form["medical_condition"],
        "symptoms" : request.form["symptoms"],
        "goals" : request.form["goals"],
        "barriers" : request.form["barriers"],
        "expected_results" : request.form["expected_results"],
        "provider_id" : provider_id,
    }

    Patient.save(data)
    print(data)
    return redirect("/dashboard")



@app.route("/patients/<int:patient_id>")
def get_one(patient_id):
    if "provider_id" not in session:
        return redirect("/")
    provider_id = session["provider_id"]

    patient = Patient.get_by_id(patient_id)
    print("inside get one")
    print(patient)
    return render_template("readone.html", patient=patient)

@app.route("/patients/edit/<int:patient_id>")
def edit_patient(patient_id):
    if "provider_id" not in session:
        return redirect("/")
    provider_id = session["provider_id"]
    patient = Patient.get_by_id(patient_id)
    return render_template("edit_patient.html", patient=patient)

@app.route("/patients/edit/<int:patient_id>", methods=["POST"])
def update(patient_id):
    if "provider_id" not in session:
        return redirect("/")
    provider_id = session["provider_id"]
    print("update")

    if not Patient.validate_patient(request.form):
        return redirect(f"/patients/edit/{patient_id}")

    patient_data = {
        "id": patient_id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "age": request.form["age"],
        "language": request.form["language"],
        "gender": request.form["gender"],
        "insurance": request.form["insurance"],
        "date_enrolled": request.form["date_enrolled"],
        "medical_condition": request.form["medical_condition"],
        "symptoms": request.form["symptoms"],
        "goals": request.form["goals"],
        "barriers": request.form["barriers"],
        "expected_results": request.form["expected_results"],
        "provider_id": provider_id,
    }

    Patient.update(patient_data)
    return redirect(f"/patients/{patient_id}")


@app.route("/patient/<int:patient_id>/destroy")
def delete_patient(patient_id):
    print("inside destroy")
    Patient.delete(patient_id)
    return redirect("/dashboard")