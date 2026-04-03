import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector

# ------------------ DATABASE CONNECTION ------------------
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_NAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

cursor = db.cursor()

# ------------------ HELPER FUNCTIONS ------------------

# Simple symptom-based disease prediction
def predict_disease(fever, cough, chest_pain, fatigue):
    if fever and cough:
        return "Flu"
    elif chest_pain:
        return "Heart Disease"
    elif fatigue and not fever:
        return "Anemia"
    else:
        return "General Illness"

# Severity detection
def detect_severity(fever, chest_pain):
    if fever and chest_pain:
        return "Serious"
    elif fever or chest_pain:
        return "Moderate"
    else:
        return "Mild"

# Suggest medicines from database
def suggest_medicine(disease):
    cursor.execute("SELECT medicine FROM medicines WHERE disease=%s", (disease,))
    meds = cursor.fetchall()
    if meds:
        return ", ".join([m[0] for m in meds])
    return "No medicine found"

# ------------------ PATIENT MENU ------------------
def patient_menu(patient_email):
    cursor.execute("SELECT patient_id, name FROM patients WHERE email=%s", (patient_email,))
    patient = cursor.fetchone()
    if not patient:
        print("Patient not found!")
        return
    patient_id, patient_name = patient
    while True:
        print(f"\n=== Welcome {patient_name} (Patient) ===")
        print("1. View my medical history")
        print("2. View my prescriptions")
        print("3. Book an appointment")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            cursor.execute("SELECT * FROM medical_history WHERE patient_id=%s", (patient_id,))
            rows = cursor.fetchall()
            if rows:
                for r in rows:
                    print(r)
            else:
                print("No medical history found.")
        elif choice == "2":
            cursor.execute("""
                SELECT p.prescription_id, p.medicines, p.dosage, p.duration, p.doctor_notes
                FROM prescriptions p
                JOIN appointments a ON p.appointment_id=a.appointment_id
                WHERE a.patient_id=%s
            """, (patient_id,))
            rows = cursor.fetchall()
            if rows:
                for r in rows:
                    print(r)
            else:
                print("No prescriptions found.")
        elif choice == "3":
            doctor_id = input("Enter Doctor ID to book appointment: ")
            date = input("Enter date (YYYY-MM-DD): ")
            time = input("Enter time (HH:MM:SS): ")
            cursor.execute(
                "INSERT INTO appointments (patient_id, doctor_id, date, time, status) VALUES (%s,%s,%s,%s,%s)",
                (patient_id, doctor_id, date, time, "Pending")
            )
            db.commit()
            print("Appointment booked (Pending Approval)")
        elif choice == "4":
            break
        else:
            print("Invalid choice!")

# ------------------ DOCTOR MENU ------------------
def doctor_menu(doctor_email):
    cursor.execute("SELECT doctor_id, name FROM doctors WHERE email=%s", (doctor_email,))
    doctor = cursor.fetchone()
    if not doctor:
        print("Doctor not found!")
        return
    doctor_id, doctor_name = doctor
    while True:
        print(f"\n=== Welcome {doctor_name} (Doctor) ===")
        print("1. View appointments")
        print("2. Predict disease & add prescription")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            cursor.execute("SELECT * FROM appointments WHERE doctor_id=%s", (doctor_id,))
            rows = cursor.fetchall()
            if rows:
                for r in rows:
                    print(r)
            else:
                print("No appointments found.")
        elif choice == "2":
            appointment_id = input("Enter appointment ID: ")
            fever = int(input("Fever (1/0): "))
            cough = int(input("Cough (1/0): "))
            chest_pain = int(input("Chest Pain (1/0): "))
            fatigue = int(input("Fatigue (1/0): "))
            disease = predict_disease(fever, cough, chest_pain, fatigue)
            severity = detect_severity(fever, chest_pain)
            medicines = suggest_medicine(disease)
            print(f"Disease Predicted: {disease}")
            print(f"Severity: {severity}")
            print(f"Suggested Medicines: {medicines}")

            dosage = input("Enter dosage (e.g., Once daily): ")
            duration = input("Enter duration (e.g., 5 days): ")
            notes = input("Enter doctor notes: ")

            cursor.execute("""
                INSERT INTO prescriptions (appointment_id, medicines, dosage, duration, doctor_notes)
                VALUES (%s,%s,%s,%s,%s)
            """, (appointment_id, medicines, dosage, duration, notes))
            db.commit()
            print("Prescription added!")
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

# ------------------ MAIN INTERFACE ------------------
if __name__ == "__main__":
    print("=== SMART DOCTOR APPOINTMENT SYSTEM ===")
    while True:
        print("\nSelect your role:")
        print("1. Patient")
        print("2. Doctor")
        print("3. Exit")
        role = input("Enter choice: ")
        if role == "1":
            email = input("Enter your registered email: ")
            patient_menu(email)
        elif role == "2":
            email = input("Enter your registered email: ")
            doctor_menu(email)
        elif role == "3":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice!")