import mysql.connector

# Database connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="newp",
    database="MediFit"
)
cursor = connection.cursor()

# Insert Data
try:
    # Populate USER Table
    cursor.executemany("""
    INSERT INTO USER (FirstName, LastName, Gender, DateOfBirth, Weight, Height, BloodGroup, Location)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, [
        ('John', 'Doe', 'Male', '1985-06-15', 75.5, 180, 'O+', 'New York'),
        ('Jane', 'Smith', 'Female', '1990-03-22', 62.3, 165, 'A-', 'Los Angeles'),
        ('Michael', 'Johnson', 'Male', '1978-11-30', 85.0, 190, 'B+', 'Chicago'),
        ('Emily', 'Williams', 'Female', '1992-09-10', 58.7, 160, 'AB+', 'Houston'),
        ('David', 'Brown', 'Male', '1983-04-05', 80.2, 175, 'O-', 'Phoenix')
    ])

    # Populate DISEASE Table (Modified to include Symptoms as a column)
    cursor.executemany("""
    INSERT INTO DISEASE (DiseaseName, Severity, TriggeringEnvironment, Communicability, Symptoms)
    VALUES (%s, %s, %s, %s, %s);
    """, [
        ('Cancer', 6, 'Smoking, radiation exposure', 'Low', 'High Blood Pressure, Fatigue, Weight Loss'),
        ('Type 2 Diabetes', 7, 'Obesity, sedentary lifestyle', 'Low', 'Frequent Thirst, Increased Hunger, Fatigue'),
        ('Common Cold', 3, 'Viral transmission, cold weather', 'Medium', 'Runny Nose, Sore Throat, Cough'),
        ('Seasonal Allergies', 4, 'Pollen, dust', 'Low', 'Itchy Eyes, Sneezing, Runny Nose'),
        ('COVID-19', 8, 'Respiratory droplets', 'High', 'Fever, Cough, Shortness of Breath')
    ])

    # Populate PRESCRIBED_TREATMENTS Table
    cursor.executemany("""
    INSERT INTO PRESCRIBED_TREATMENTS (DiseaseID, TypeOfTreatment, Description, Expense, CureTime, SourceOfPrescription)
    VALUES (%s, %s, %s, %s, %s, %s);
    """, [
        (1, 'Allopathy', 'Lifestyle changes and medication', 200.00, '6 months', 'Dr. Smith'),
        (2, 'Allopathy', 'Insulin therapy and diet control', 300.00, 'Lifetime management', 'Dr. Johnson'),
        (3, 'Homeopathy', 'Immune support remedies', 50.00, '1 week', 'Dr. Adams'),
        (4, 'Ayurveda', 'Herbal remedies', 100.00, 'Seasonal', 'Dr. Patel'),
        (5, 'Allopathy', 'Vaccination and antivirals', 500.00, '2 weeks', 'Dr. Taylor')
    ])

    # Populate MEDICATION Table
    cursor.executemany("""
    INSERT INTO MEDICATION (DiseaseID, MedicationName, TypeOfTreatment, FoodRestrictionConditions)
    VALUES (%s, %s, %s, %s);
    """, [
        (1, 'Amlodipine', 'Allopathy', 'Avoid grapefruit'),
        (2, 'Metformin', 'Allopathy', 'Avoid alcohol'),
        (3, 'Antihistamines', 'Allopathy', 'Avoid heavy machinery'),
        (4, 'Ashwagandha', 'Ayurveda', 'Avoid spicy foods'),
        (5, 'Favipiravir', 'Allopathy', 'Take with food')
    ])

    # Populate TEST_REPORTS Table
    cursor.executemany("""
    INSERT INTO TEST_REPORTS (UserID, TreatmentID, TestType, TestReport, OrganizationLab, DoctorOnConsultation, TestDate)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, [
        (1, 1, 'Blood Pressure Test', 'Normal', 'LabCorp', 'Dr. Smith', '2024-01-10'),
        (2, 2, 'HbA1c Test', 'High glucose levels', 'Quest Diagnostics', 'Dr. Johnson', '2024-02-15'),
        (3, 3, 'Nasal Swab', 'Positive for cold virus', 'CityLab', 'Dr. Adams', '2024-03-20'),
        (4, 4, 'Allergy Skin Test', 'Positive for pollen allergy', 'AllergyClinic', 'Dr. Patel', '2024-04-25'),
        (5, 5, 'RT-PCR', 'Positive for COVID-19', 'PathCare', 'Dr. Taylor', '2024-05-30')
    ])

    # Populate MEDICAL_HISTORY Table
    cursor.executemany("""
    INSERT INTO MEDICAL_HISTORY (UserID, Allergies, GeneticCharacteristics)
    VALUES (%s, %s, %s);
    """, [
        (1, 'Peanuts', 'Hypertension in family'),
        (2, 'None', 'Diabetes in family'),
        (3, 'Penicillin', 'None'),
        (4, 'Pollen', 'None'),
        (5, 'None', 'Heart disease in family')
    ])

    # Populate UNDERGOING_TREATMENTS Table
    cursor.executemany("""
    INSERT INTO UNDERGOING_TREATMENTS (UserID, TreatmentID, DiseaseID, AssociatedHospital, DoctorUnderConsultation, Status, Description, AgeAtTreatmentStart)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, [
        (1, 1, 1, 'City Hospital', 'Dr. Smith', 'Ongoing', 'Hypertension management', 38),
        (2, 2, 2, 'State Clinic', 'Dr. Johnson', 'Ongoing', 'Diabetes management', 34),
        (3, 3, 3, 'Local Health Center', 'Dr. Adams', 'Completed', 'Common cold treatment', 45),
        (4, 4, 4, 'Natural Remedies Hospital', 'Dr. Patel', 'Completed', 'Allergy relief', 32),
        (5, 5, 5, 'Community Health Facility', 'Dr. Taylor', 'Ongoing', 'COVID-19 care', 40)
    ])

    # Commit changes
    connection.commit()
    print("All data inserted successfully into all tables.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    connection.close()
