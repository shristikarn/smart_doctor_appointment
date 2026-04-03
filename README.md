# smart_doctor_appointment

A Python + MySQL based healthcare management system that simulates real-world doctor-patient interactions.  
Patients can book appointments, doctors can manage them, and a simple rule-based AI predicts diseases based on symptoms.

## Features

### Patient Module
- View personal medical history  
- View prescriptions given by doctors  
- Book appointments with available doctors  
- Interactive menu-based system  

### Doctor Module
- View assigned appointments  
- Predict disease based on patient symptoms  
- Detect severity of illness (Mild / Moderate / Serious)  
- Suggest medicines automatically from database  
- Add prescriptions with dosage, duration, and notes  

### Smart Prediction
- Simple rule-based disease prediction using:
  - Fever  
  - Cough  
  - Chest Pain  
  - Fatigue  

##  Database Design

The system uses a MySQL relational database with the following tables:

- *patients* – Stores patient details  
- *doctors* – Stores doctor information and specialization  
- *appointments* – Manages booking between patients and doctors  
- *prescriptions* – Stores medicines, dosage, and doctor notes  
- *medical_history* – Tracks past diseases and treatments  
- *medicines* – Maps diseases to medicines  
- *symptoms_data* – Stores symptom combinations for analysis  

## Technologies Used
- Python (Core Logic)
- MySQL (Database)
- mysql-connector-python (Database Connectivity)

##  Sample Data
- 120+ Patients  
- 25 Doctors  
- 150 Appointments  
- 200 Prescriptions  
- Medical history and symptoms dataset  

##  How to Run
1. Clone the repository  
2. Install dependencies:
   ```bash
   pip install mysql-connector-python
