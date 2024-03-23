from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
from datetime import datetime

from flask_app.models import provider


import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class Patient:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.age = data["age"]
        self.language = data["language"]
        self.gender = data["gender"]
        self.insurance = data["insurance"]
        self.date_enrolled = data["date_enrolled"]
        self.medical_condition = data["medical_condition"]
        self.symptoms = data["symptoms"]
        self.goals = data["goals"]
        self.barriers = data["barriers"]
        self.expected_results = data["expected_results"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.provider_id = data["provider_id"]

        self.doctor = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM patients LEFT JOIN providers ON providers.id = patients.provider_id"
        results = connectToMySQL("providers_and_patients").query_db(query)
        print("results")
        print(results)
        all_patients = []

        for r in results:
            patient = cls(r)
            patient.doctor = provider.Provider(
                {
                    "id": r["provider_id"],
                    "first_name": r["providers.first_name"],
                    "last_name": r["providers.last_name"],
                    "email": r["providers.email"],
                    "password": r["password"],
                    "created_at": r["providers.created_at"],
                    "updated_at": r["providers.updated_at"],
                }
            )
            all_patients.append(patient)

        print("hi")
        print(all_patients)
        return all_patients

    @classmethod
    def save(cls, data):
        query = "INSERT INTO patients (first_name, last_name, email, age, language, gender, insurance, date_enrolled, medical_condition, symptoms, goals, barriers, expected_results, provider_id) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(age)s, %(language)s, %(gender)s, %(insurance)s, %(date_enrolled)s, %(medical_condition)s, %(symptoms)s, %(goals)s, %(barriers)s, %(expected_results)s, %(provider_id)s);"
        print("here")
        return connectToMySQL("providers_and_patients").query_db(query, data)

    # @classmethod
    # def get_by_id(cls, id):
    #     query = "SELECT * FROM patients LEFT JOIN providers ON providers.id = patients.provider_id"
    #     data = {"id": id}
    #     results = connectToMySQL("providers_and_patients").query_db(query, data)
    #     if not results: 
    #         return None
        
    #     patient_data = results[0]
    #     print(patient_data)
    #     patient = cls(patient_data)

    #     provider_data = {
    #     "id": patient_data["provider_id"],
    #     "first_name": patient_data["providers.first_name"],
    #     "last_name": patient_data["providers.last_name"],
    #     "email": patient_data["providers.email"],
    #     "password": patient_data["password"],
    #     "created_at": patient_data["providers.created_at"],
    #     "updated_at": patient_data["providers.updated_at"],
    # }
    #     patient.doctor = provider.Provider(provider_data)

    #     return patient
    
            # query = "SELECT * FROM patients WHERE patients.id = %(id)s;"
            # data = {"id": id}
            # results = connectToMySQL("providers_and_patients").query_db(query, data)
            # print("inside get by id")
            # print(results[0])
            # return cls(results[0])
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM patients LEFT JOIN providers ON providers.id = patients.provider_id WHERE patients.id = %(id)s"
        data = {"id": id}
        results = connectToMySQL("providers_and_patients").query_db(query, data)
        if not results: 
            return None
        
        patient_data = results[0]
        print(patient_data)
        patient = cls(patient_data)

        provider_data = {
        "id": patient_data["provider_id"],
        "first_name": patient_data["providers.first_name"],
        "last_name": patient_data["providers.last_name"],
        "email": patient_data["providers.email"],
        "password": patient_data["password"],
        "created_at": patient_data["providers.created_at"],
        "updated_at": patient_data["providers.updated_at"],
    }
        patient.doctor = provider.Provider(provider_data)

       
        return patient
        # print("inside get by id")
        # print(results[0])

        # return cls(results[0])
    
 
    @classmethod
    def update(cls, data):
        query = """
            UPDATE
                patients
            SET
                first_name = %(first_name)s,
                last_name = %(last_name)s,
                email = %(email)s,
                age = %(age)s,
                language = %(language)s,
                gender = %(gender)s,
                insurance = %(insurance)s,
                date_enrolled = %(date_enrolled)s,
                medical_condition = %(medical_condition)s,
                symptoms = %(symptoms)s,
                goals = %(goals)s,
                barriers = %(barriers)s,
                expected_results = %(expected_results)s
                
                
                
            WHERE
                patients.id = %(id)s;
        """
        results = connectToMySQL("providers_and_patients").query_db(query, data)
        # print(results)
        return results

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM patients WHERE patients.id = %(id)s;"
        data = {"id": id}
        return connectToMySQL("providers_and_patients").query_db(query, data)

    @staticmethod
    def validate_patient(patient):
        is_valid = True
        if len(patient["first_name"]) < 3:
            flash("First name is required and must atleast be 3 characters")
            is_valid = False

        if len(patient["last_name"]) < 3:
            flash("First name is required and must atleast be 3 characters")
            is_valid = False

        if not EMAIL_REGEX.match(patient["email"]):
            flash("Email address is not valid!")
            if len(patient["email"]) < 1:
                flash("Email address cannot be blank!")
            is_valid = False

        if int(patient["age"]) < 1:
            flash("Please enter the age of the patient")
            is_valid = False

        if not "language" in patient or not patient["language"]:
            flash("Please select a language option.")
            is_valid = False

        if not "gender" in patient or not patient["gender"]:
            flash("Please select a gender option.")
            is_valid = False

        if not "insurance" in patient or not patient["insurance"]:
            flash("Please select an insurance option.")
            is_valid = False

        c_time = datetime.now()
        current_date = c_time.strftime("%Y-%m-%d")
        print("current time is", current_date)
        print("time to compare is", patient["date_enrolled"])
        if (patient["date_enrolled"]) > current_date:
            flash("Enter a Valid Date")
            is_valid = False

        if len(patient["medical_condition"]) < 3:
            flash("Describe medical condition in atleast 3 characters")
            is_valid = False

        if len(patient["symptoms"]) < 3:
            flash("Describe symptoms in atleast 3 characters")
            is_valid = False

        if len(patient["goals"]) < 3:
            flash("Describe goals in atleast 3 characters")
            is_valid = False

        if len(patient["barriers"]) < 3:
            flash("Describe barriers in atleast 3 characters")
            is_valid = False

        if len(patient["expected_results"]) < 3:
            flash("Describe results in atleast 3 characters")
            is_valid = False

        return is_valid
