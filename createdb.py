import mysql.connector

def create_schema():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="newp"  # Replace with your MySQL root password
        )
        cursor = connection.cursor()

        # List of schema creation commands
        schema_commands = [
            "CREATE DATABASE IF NOT EXISTS MediFit;",
            "USE MediFit;",
            """
            CREATE TABLE USER (
                UserID INT PRIMARY KEY AUTO_INCREMENT,
                FirstName VARCHAR(50) NOT NULL,
                LastName VARCHAR(50) NOT NULL,
                Gender ENUM('Male', 'Female', 'Other'),
                DateOfBirth DATE,
                Weight DECIMAL(5,2) NOT NULL,
                Height DECIMAL(5,2) NOT NULL,
                BloodGroup VARCHAR(5) NOT NULL,
                Location VARCHAR(100)
            );
            """,
            """
            CREATE TABLE DISEASE (
                DiseaseID INT PRIMARY KEY AUTO_INCREMENT,
                DiseaseName VARCHAR(100) NOT NULL,
                Severity INT CHECK (Severity BETWEEN 1 AND 10),
                TriggeringEnvironment TEXT,
                Communicability ENUM('Low', 'Medium', 'High') NOT NULL,
                Symptoms TEXT  -- Added Symptoms column directly to the DISEASE table
            );
            """,
            """
            CREATE TABLE PRESCRIBED_TREATMENTS (
                TreatmentID INT PRIMARY KEY AUTO_INCREMENT,
                DiseaseID INT,
                TypeOfTreatment ENUM('Homeopathy', 'Allopathy', 'Ayurveda', 'Chiropractic', 'TCM'),
                Description TEXT,
                Expense DECIMAL(10,2),
                CureTime VARCHAR(50),
                SourceOfPrescription VARCHAR(100) NOT NULL,
                FOREIGN KEY (DiseaseID) REFERENCES DISEASE(DiseaseID)
            );
            """,
            """
            CREATE TABLE MEDICATION (
                MedicationID INT PRIMARY KEY AUTO_INCREMENT,
                DiseaseID INT,
                MedicationName VARCHAR(100) NOT NULL,
                TypeOfTreatment ENUM('Homeopathy', 'Allopathy', 'Ayurveda', 'Chiropractic', 'TCM'),
                FoodRestrictionConditions TEXT,
                FOREIGN KEY (DiseaseID) REFERENCES DISEASE(DiseaseID)
            );
            """,
            """
            CREATE TABLE TEST_REPORTS (
                TestID INT PRIMARY KEY AUTO_INCREMENT,
                UserID INT,
                TreatmentID INT,
                TestType VARCHAR(50) NOT NULL,
                TestReport TEXT,
                OrganizationLab VARCHAR(100),
                DoctorOnConsultation VARCHAR(100) NOT NULL,
                TestDate DATE,
                FOREIGN KEY (UserID) REFERENCES USER(UserID),
                FOREIGN KEY (TreatmentID) REFERENCES PRESCRIBED_TREATMENTS(TreatmentID)
            );
            """,
            """
            CREATE TABLE MEDICAL_HISTORY (
                UserID INT,
                Allergies TEXT,
                GeneticCharacteristics TEXT,
                PRIMARY KEY (UserID),
                FOREIGN KEY (UserID) REFERENCES USER(UserID)
            );
            """,
            """
            CREATE TABLE UNDERGOING_TREATMENTS (
                UserID INT,
                TreatmentID INT,
                DiseaseID INT,
                AssociatedHospital VARCHAR(100),
                DoctorUnderConsultation VARCHAR(100),
                Status ENUM('Ongoing', 'Completed'),
                Description TEXT,
                AgeAtTreatmentStart INT,
                PRIMARY KEY (UserID, TreatmentID),
                FOREIGN KEY (UserID) REFERENCES USER(UserID),
                FOREIGN KEY (TreatmentID) REFERENCES PRESCRIBED_TREATMENTS(TreatmentID),
                FOREIGN KEY (DiseaseID) REFERENCES DISEASE(DiseaseID)
            );
            """
        ]

        # Execute each command separately
        for command in schema_commands:
            cursor.execute(command)
        
        print("Schema created successfully.")

    except mysql.connector.Error as error:
        print(f"Error: {error}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_schema()
