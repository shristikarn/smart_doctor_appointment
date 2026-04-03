import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector
import random

# ------------------ DATABASE CONNECTION ------------------
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_NAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
    )

cursor = db.cursor()

# ------------------ 1. INSERT PATIENTS ------------------
first_names = ["Rahul","Amit","Priya","Neha","Arjun","Kavita","Rohan","Sneha"]
last_names = ["Sharma","Das","Gupta","Singh","Verma","Yadav","Roy"]

for i in range(120):
    name = random.choice(first_names) + " " + random.choice(last_names)
    age = random.randint(18,60)
    gender = random.choice(["Male","Female"])
    email = f"user{i}@gmail.com"
    cursor.execute("SELECT * from patients where email=%s",(email,))
    result=cursor.fetchone()
    if result:
        continue

    cursor.execute("""
        INSERT INTO patients (name, age, gender, email, password)
        VALUES (%s,%s,%s,%s,%s)
    """,(name, age, gender, email, "pass123"))

db.commit()
print("Patients inserted")

# ------------------ 2. INSERT DOCTORS ------------------
specializations = ["Cardiologist","Dermatologist","Neurologist","Orthopedic","General"]

for i in range(25):
    name = f"Dr. Doctor{i}"
    spec = random.choice(specializations)
    email = f"doctor{i}@gmail.com"

    cursor.execute("""
        INSERT INTO doctors (name, specialization, email, password)
        VALUES (%s,%s,%s,%s)
    """,(name, spec, email, "pass123"))

db.commit()
print("Doctors inserted")

# ------------------ 3. INSERT APPOINTMENTS ------------------
for i in range(150):
    patient_id = random.randint(1,120)
    doctor_id = random.randint(1,25)

    date = f"2026-04-{random.randint(1,28):02d}"
    time = f"{random.randint(9,17):02d}:00:00"
    status = random.choice(["Pending","Approved","Rejected"])

    cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_id, date, time, status)
        VALUES (%s,%s,%s,%s,%s)
    """,(patient_id, doctor_id, date, time, status))

db.commit()
print("Appointments inserted")

# ------------------ 4. INSERT MEDICINES ------------------
medicine_data = [
    ("Flu","Paracetamol","500mg"),
    ("Cold","Cough Syrup","10ml"),
    ("COVID-19","Paracetamol","650mg"),
    ("Heart Disease","Aspirin","75mg"),
    ("Diabetes","Metformin","500mg"),
    ("Hypertension","Amlodipine","5mg"),
    ("Asthma","Salbutamol","2 puffs"),
    ("Pneumonia","Azithromycin","500mg"),
    ("Migraine","Sumatriptan","50mg"),
    ("Food Poisoning","ORS","1 sachet")
]

for data in medicine_data:
    cursor.execute("""
        INSERT INTO medicines (disease, medicine, dosage)
        VALUES (%s,%s,%s)
    """, data)

db.commit()
print("Medicines inserted")

# ------------------ 5. INSERT PRESCRIPTIONS ------------------
notes_list = [
    "Take medicines after food",
    "Drink plenty of water",
    "Avoid cold drinks",
    "Complete full course",
    "Take rest for 3 days",
    "Monitor blood pressure daily",
    "Avoid stress",
    "Use inhaler regularly"
]

durations = ["3 days","5 days","7 days","10 days"]

for i in range(200):
    appointment_id = random.randint(1,150)

    cursor.execute("SELECT medicine FROM medicines ORDER BY RAND() LIMIT 2")
    meds = cursor.fetchall()
    med_names = ", ".join([m[0] for m in meds])

    cursor.execute("""
        INSERT INTO prescriptions 
        (appointment_id, doctor_notes, medicines, dosage, duration)
        VALUES (%s,%s,%s,%s,%s)
    """,(appointment_id,
         random.choice(notes_list),
         med_names,
         random.choice(["Once daily","Twice daily"]),
         random.choice(durations)))

db.commit()
print("Prescriptions inserted")

# ------------------ 6. INSERT MEDICAL HISTORY ------------------
diseases = ["Flu","Cold","COVID-19","Heart Disease","Diabetes",
            "Hypertension","Asthma","Migraine","Pneumonia"]

severity_levels = ["Mild","Moderate","Severe"]

for i in range(200):
    patient_id = random.randint(1,120)

    cursor.execute("""
        INSERT INTO medical_history 
        (patient_id, disease, severity, treatment, doctor_name, date)
        VALUES (%s,%s,%s,%s,%s,%s)
    """,(patient_id,
         random.choice(diseases),
         random.choice(severity_levels),
         "Standard Treatment",
         f"Dr. {random.randint(1,25)}",
         f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}"))

db.commit()
print("Medical history inserted")

# ------------------ 7. INSERT SYMPTOMS DATA ------------------
for i in range(300):
    cursor.execute("""
        INSERT INTO symptoms_data 
        (fever, cough, chest_pain, fatigue, headache, nausea, breathlessness, disease)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """,(random.randint(0,1),
         random.randint(0,1),
         random.randint(0,1),
         random.randint(0,1),
         random.randint(0,1),
         random.randint(0,1),
         random.randint(0,1),
         random.choice(diseases)))

db.commit()
print("Symptoms data inserted")

print( "ALL DATA INSERTED SUCCESSFULLY")