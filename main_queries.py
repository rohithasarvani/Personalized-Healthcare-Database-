import pymysql
import datetime

class MediFitCLI:
   def __init__(self):
      try:
         self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='newp',
            database='MediFit'
         )
         self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
      except pymysql.Error as e:
         print(f"Error connecting to database: {e}")
         exit(1)

   def close_connection(self):
      self.connection.close()

   # Retrieval Methods
   def retrieve_users_by_blood_group(self, blood_group='O+'):
      """Retrieve all users with a specific blood group (Selection Query)"""
      try:
         query = "SELECT * FROM USER WHERE BloodGroup = %s"
         self.cursor.execute(query, (blood_group,))
         return self.cursor.fetchall()
      except pymysql.Error as e:
         print(f"Error retrieving users: {e}")
         return []

   def retrieve_users_by_ongoing_treatments(self):
      """Retrieve all users who are currently undergoing treatment (Selection Query)"""
      try:
         query = """
         SELECT u.* 
         FROM USER u
         JOIN UNDERGOING_TREATMENTS ut ON u.UserID = ut.UserID
         WHERE ut.Status = 'Ongoing'
         """
         self.cursor.execute(query)
         return self.cursor.fetchall()
      except pymysql.Error as e:
         print(f"Error retrieving ongoing treatments: {e}")
         return []

   def retrieve_mri_test_reports(self, years=1):
      """Retrieve details of all users who have undergone an MRI test in the last year (Selection Query)"""
      try:
         query = """
         SELECT u.*, tr.*
         FROM USER u
         JOIN TEST_REPORTS tr ON u.UserID = tr.UserID
         WHERE tr.TestType = 'MRI' AND tr.TestDate >= DATE_SUB(CURDATE(), INTERVAL %s YEAR)
         """
         self.cursor.execute(query, (years,))
         return self.cursor.fetchall()
      except pymysql.Error as e:
         print(f"Error retrieving MRI test reports: {e}")
         return []

   # Projection Queries
   def retrieve_users_location_by_blood_group(self, blood_group='A-'):
      """Retrieve names and geographic locations of users with specific blood group (Projection Query)"""
      try:
         query = "SELECT FirstName, LastName, Location FROM USER WHERE BloodGroup = %s"
         self.cursor.execute(query, (blood_group,))
         return self.cursor.fetchall()
      except pymysql.Error as e:
         print(f"Error retrieving user locations: {e}")
         return []

   def retrieve_allopathy_diseases(self):
      """Retrieve disease names for Allopathy treatments (Projection Query)"""
      try:
         query = """
         SELECT DISTINCT d.DiseaseName
         FROM DISEASE d
         JOIN PRESCRIBED_TREATMENTS pt ON d.DiseaseID = pt.DiseaseID
         WHERE pt.TypeOfTreatment = 'Allopathy'
         """
         self.cursor.execute(query)
         return self.cursor.fetchall()
      except pymysql.Error as e:
         print(f"Error retrieving Allopathy diseases: {e}")
         return []

   # Aggregate Function Queries
   def calculate_comprehensive_metrics(self):
      """Comprehensive aggregate metrics (Aggregate Function Queries)"""
      try:
         # Average expense of cancer treatments
         cancer_expense_query = """
         SELECT AVG(pt.Expense) as AverageCancerTreatmentExpense
         FROM PRESCRIBED_TREATMENTS pt
         JOIN DISEASE d ON pt.DiseaseID = d.DiseaseID
         WHERE d.DiseaseName LIKE '%Cancer%'
         """
         self.cursor.execute(cancer_expense_query)
         cancer_expense = self.cursor.fetchone()

         # Maximum severity of diseases
         max_severity_query = "SELECT MAX(Severity) as MaxDiseaseSeverity FROM DISEASE"
         self.cursor.execute(max_severity_query)
         max_severity = self.cursor.fetchone()

         # Total ongoing treatments
         ongoing_treatments_query = """
         SELECT COUNT(*) as TotalOngoingTreatments
         FROM UNDERGOING_TREATMENTS
         WHERE Status = 'Ongoing'
         """
         self.cursor.execute(ongoing_treatments_query)
         ongoing_treatments = self.cursor.fetchone()

         return {
               **cancer_expense,
               **max_severity,
               **ongoing_treatments
         }
      except pymysql.Error as e:
         print(f"Error calculating metrics: {e}")
         return None

   def get_average_bmi(self):
    try:
        query = """
        SELECT AVG(Weight / (Height * Height)) as AverageBMI
        FROM USER
        WHERE Height IS NOT NULL AND Weight IS NOT NULL
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()
    except pymysql.Error as e:
        print(f"Error calculating average BMI: {e}")
        return None


   def get_average_cancer_treatment_expense(self):
      try:
         query = """
         SELECT AVG(pt.Expense) as average 
         FROM PRESCRIBED_TREATMENTS pt
         JOIN DISEASE d ON pt.DiseaseID = d.DiseaseID
         WHERE d.DiseaseName LIKE '%Cancer%'
         """
         self.cursor.execute(query)
         return self.cursor.fetchone()
      except pymysql.Error as e:
         print(f"Error calculating average cancer treatment expense: {e}")
         return None

   def get_max_severity_of_diseases(self):
      try:
         query = "SELECT MAX(Severity) as MaxSeverity FROM DISEASE"
         self.cursor.execute(query)
         return self.cursor.fetchone()
      except pymysql.Error as e:
         print(f"Error finding maximum severity of diseases: {e}")
         return None

   def get_total_ongoing_treatments(self):
      try:
         query = """
         SELECT COUNT(*) as TotalOngoingTreatments
         FROM UNDERGOING_TREATMENTS
         WHERE Status = 'Ongoing'
         """
         self.cursor.execute(query)
         return self.cursor.fetchone()
      except pymysql.Error as e:
         print(f"Error finding total ongoing treatments: {e}")
         return None


   # Search Queries
   def search_users_by_name_prefix(self, prefix='Jo'):
      """Search for users with first name starting with a prefix (Search Query)"""
      try:
         query = "SELECT * FROM USER WHERE FirstName LIKE %s"
         self.cursor.execute(query, (f"{prefix}%",))
         return self.cursor.fetchall()
      except pymysql.Error as e:
         print(f"Error searching users by name: {e}")
         return []

   def search_test_reports_by_type(self, test_type='CT'):
      """Search for test reports related to a specific type (Search Query)"""
      try:
         query = """
         SELECT tr.*
         FROM TEST_REPORTS tr
         WHERE tr.TestType LIKE %s
         """
         self.cursor.execute(query, (f"%{test_type}%",))
         return self.cursor.fetchall()
      except pymysql.Error as e:
         print(f"Error searching test reports: {e}")
         return []

   def search_diseases_by_symptom(self, symptom='cough'):
      """Search for diseases whose symptoms contain a specific word (Search Query)"""
      try:
         query = "SELECT * FROM DISEASE WHERE Symptoms LIKE %s"
         self.cursor.execute(query, (f"%{symptom}%",))
         return self.cursor.fetchall()
      except pymysql.Error as e:
         print(f"Error searching diseases by symptom: {e}")
         return []

   # Analysis Queries
   def analyze_high_severity_treatments(self, severity_threshold=7):
      """Find number of users with ongoing treatments for high-severity diseases"""
      try:
         query = """
         SELECT COUNT(DISTINCT u.UserID) as UserCount
         FROM USER u
         JOIN UNDERGOING_TREATMENTS ut ON u.UserID = ut.UserID
         JOIN DISEASE d ON ut.DiseaseID = d.DiseaseID
         WHERE ut.Status = 'Ongoing' AND d.Severity > %s
         """
         self.cursor.execute(query, (severity_threshold,))
         return self.cursor.fetchone()
      except pymysql.Error as e:
         print(f"Error analyzing high severity treatments: {e}")
         return None

   def analyze_allopathy_treatments(self):
      """Find number of patients undergoing Allopathy treatments in the last 'years' year"""
      try:
         query = """
         SELECT COUNT(*) AS PatientCount
            FROM PRESCRIBED_TREATMENTS
            WHERE TypeOfTreatment = 'Allopathy'"""
         self.cursor.execute(query)
         return self.cursor.fetchone()
      except pymysql.Error as e:
         print(f"Error analyzing Allopathy treatments: {e}")
         return None

   # Modification Methods
   def insert_new_user(self, first_name, last_name, blood_group, gender=None, 
                     date_of_birth=None, weight=None, height=None, location=None):
      """Insert a new user into the USER table"""
      try:
         # Validate blood group (required constraint)
         if not blood_group:
               raise ValueError("Blood Group must be provided")

         query = """
         INSERT INTO USER 
         (FirstName, LastName, BloodGroup, Gender, DateOfBirth, Weight, Height, Location) 
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
         """
         self.cursor.execute(query, (
               first_name, last_name, blood_group, gender, 
               date_of_birth, weight, height, location
         ))
         self.connection.commit()
         return self.cursor.lastrowid
      except pymysql.Error as e:
         print(f"Error inserting new user: {e}")
         self.connection.rollback()
         return None

   def insert_new_disease(self, disease_name, severity, communicability, 
                       triggering_environment=None):
    """Insert a new disease into the DISEASE table"""
    try:
        # Validate communicability (required constraint)
        if communicability is None:
            raise ValueError("Communicability must be specified")

        query = """
        INSERT INTO DISEASE 
        (DiseaseName, Severity, Communicability, TriggeringEnvironment) 
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            disease_name, severity, communicability, 
            triggering_environment
        ))
        disease_id = self.cursor.lastrowid
        self.connection.commit()
        return disease_id
    except pymysql.Error as e:
        print(f"Error inserting new disease: {e}")
        self.connection.rollback()
        return None

   def update_user_weight(self, user_id, new_weight):
      """Update the weight of a user"""
      try:
         # Update weight
         update_query = """
         UPDATE USER 
         SET Weight = %s 
         WHERE UserID = %s
         """
         self.cursor.execute(update_query, (new_weight, user_id))
         self.connection.commit()
         return True
      except pymysql.Error as e:
         print(f"Error updating user weight: {e}")
         self.connection.rollback()
         return False

   def update_treatment_status(self, user_id, treatment_id, new_status='Completed'):
      """Update the status of a treatment"""
      try:
         query = """
         UPDATE UNDERGOING_TREATMENTS 
         SET Status = %s 
         WHERE UserID = %s AND TreatmentID = %s
         """
         self.cursor.execute(query, (new_status, user_id, treatment_id))
         self.connection.commit()
      except pymysql.Error as e:
         print(f"Error updating treatment status: {e}")
         self.connection.rollback()

   def delete_medication(self, medication_id):
      """Delete a discontinued/banned medication and inform affected users"""
      try:
         # Find affected users
         user_query = """
         SELECT DISTINCT u.UserID, u.FirstName, u.LastName
         FROM USER u
         JOIN UNDERGOING_TREATMENTS ut ON u.UserID = ut.UserID
         JOIN PRESCRIBED_TREATMENTS pt ON ut.TreatmentID = pt.TreatmentID
         JOIN MEDICATION m ON pt.DiseaseID = m.DiseaseID
         WHERE m.MedicationID = %s
         """
         self.cursor.execute(user_query, (medication_id,))
         affected_users = self.cursor.fetchall()

         # Delete medication
         delete_query = "DELETE FROM MEDICATION WHERE MedicationID = %s"
         self.cursor.execute(delete_query, (medication_id,))
         
         self.connection.commit()
         
         # Return list of affected users for potential notification
         return affected_users
      except pymysql.Error as e:
         print(f"Error deleting medication: {e}")
         self.connection.rollback()
         return []

def main():
   cli = MediFitCLI()

   while True:
        print("\n--- MediFit Healthcare Management System ---")
        print("\nRetrieve Information:")
        print("1. Retrieve Users by Blood Group")
        print("2. Retrieve Users with Ongoing Treatments")
        print("3. Retrieve MRI Test Reports")
        print("4. Retrieve Users Location by Blood Group")
        print("5. Retrieve Allopathy Diseases")
        print("6. Search Users by Name Prefix")
        print("7. Search Test Reports by Type")
        print("8. Search Diseases by Symptom")
        print("9. Calculate Comprehensive Health Metrics")
        print("10. Find Average BMI")
        print("11. Find Average Cancer Treatment Expense")
        print("12. Analyze High Severity Treatments")
        print("13. Analyze Allopathy Treatments")
        print("14. Insert New User")
        print("15. Insert New Disease")
        print("16. Update User Weight")
        print("17. Update Treatment Status")
        print("18. Delete Medication")
        print("19. Calculate Maximum Severity of Diseases")
        print("20. Total Ongoing Treatments")
        print("0. Exit")

        try:
            choice = int(input("\nEnter your choice: "))

            if choice == 1:
                blood_group = input("Enter Blood Group (default O+): ") or 'O+'
                results = cli.retrieve_users_by_blood_group(blood_group)
                print(f"\nUsers with {blood_group} Blood Group:")
                for user in results:
                    print(f"Name: {user['FirstName']} {user['LastName']}, Location: {user.get('Location', 'N/A')}")

            elif choice == 2:
                results = cli.retrieve_users_by_ongoing_treatments()
                print("\nUsers with Ongoing Treatments:")
                for user in results:
                    print(f"Name: {user['FirstName']} {user['LastName']}, UserID: {user['UserID']}")

            elif choice == 3:
                years = input("Enter years for MRI reports (default 1): ") or 1
                results = cli.retrieve_mri_test_reports(int(years))
                print(f"\nMRI Test Reports in the last {years} year(s):")
                for report in results:
                    print(f"Name: {report['FirstName']} {report['LastName']}, Test Time: {report['TimeOfTest']}")

            elif choice == 4:
                blood_group = input("Enter Blood Group (default A-): ") or 'A-'
                results = cli.retrieve_users_location_by_blood_group(blood_group)
                print(f"\nUsers with {blood_group} Blood Group Locations:")
                for user in results:
                    print(f"Name: {user['FirstName']} {user['LastName']}, Location: {user['Location']}")

            elif choice == 5:
                results = cli.retrieve_allopathy_diseases()
                print("\nAllopathy Diseases:")
                for disease in results:
                    print(f"{disease['DiseaseName']}")

            elif choice == 6:
                prefix = input("Enter name prefix (default 'Jo'): ") or 'Jo'
                results = cli.search_users_by_name_prefix(prefix)
                print(f"\nUsers with Name Prefix '{prefix}':")
                for user in results:
                    print(f"Name: {user['FirstName']} {user['LastName']}")

            elif choice == 7:
                test_type = input("Enter test type (default 'CT'): ") or 'CT'
                results = cli.search_test_reports_by_type(test_type)
                print(f"\nTest Reports of Type '{test_type}':")
                for report in results:
                    print(f"Test ID: {report['TestID']}, Type: {report['TestType']}")

            elif choice == 8:
                symptom = input("Enter symptom to search (default 'cough'): ") or 'cough'
                results = cli.search_diseases_by_symptom(symptom)
                print(f"\nDiseases with '{symptom}' Symptom:")
                for disease in results:
                    print(f"Disease: {disease['DiseaseName']}, Severity: {disease['Severity']}")

            elif choice == 9:
                metrics = cli.calculate_comprehensive_metrics()
                print("\nComprehensive Health Metrics:")
                for key, value in metrics.items():
                    print(f"{key}: {value}")

            elif choice == 10:
                average_bmi = cli.get_average_bmi()
                if average_bmi:
                    print(f"\nAverage BMI: {average_bmi['AverageBMI']}")

            elif choice == 11:
                average_expense = cli.get_average_cancer_treatment_expense()
                if average_expense:
                    print(f"\nAverage Cancer Treatment Expense: {average_expense['average']}")

            elif choice == 12:
                severity = input("Enter severity threshold (default 7): ") or 7
                results = cli.analyze_high_severity_treatments(int(severity))
                print(f"\nUsers with High Severity Treatments (Severity > {severity}):")
                print(f"Total Users: {results['UserCount']}")

            elif choice == 13:
                results = cli.analyze_allopathy_treatments()
                print(f"\nPatients with Allopathy Treatments: {results['PatientCount']}")

            elif choice == 14:
                first_name = input("Enter First Name: ")
                last_name = input("Enter Last Name: ")
                blood_group = input("Enter Blood Group: ")
                gender = input("Enter Gender (optional): ") or None
                dob = input("Enter Date of Birth (YYYY-MM-DD, optional): ") or None
                weight = input("Enter Weight (kg, optional): ") or None
                height = input("Enter Height (cm, optional): ") or None
                location = input("Enter Location (optional): ") or None

                user_id = cli.insert_new_user(
                    first_name, last_name, blood_group, gender, 
                    dob, float(weight) if weight else None, 
                    float(height) if height else None, location
                )
                if user_id:
                    print(f"New user added with UserID: {user_id}")

            elif choice == 15:
               disease_name = input("Enter Disease Name: ")
               severity = int(input("Enter Severity (1-10): "))
               communicability = input("Enter Communicability (Low/Medium/High): ")
               triggering_env = input("Enter Triggering Environment (optional): ") or None

               disease_id = cli.insert_new_disease(
                  disease_name, severity, communicability, triggering_env
               )
               if disease_id:
                  print(f"New disease added with DiseaseID: {disease_id}")

            elif choice == 16:
               user_id = int(input("Enter User ID: "))
               new_weight = float(input("Enter New Weight (kg): "))
               bmi = cli.update_user_weight(user_id, new_weight)
               if bmi:
                  print(f"Updated BMI: {bmi}")
               else:
                  print("Error updating BMI.")

            elif choice == 17:
               user_id = int(input("Enter User ID: "))
               treatment_id = int(input("Enter Treatment ID: "))
               status = input("Enter New Treatment Status (optional, default: 'Completed'): ") or 'Completed'
               cli.update_treatment_status(user_id, treatment_id, status)
               print(f"Treatment status updated to {status}.")

            elif choice == 18:
               medication_id = int(input("Enter Medication ID: "))
               affected_users = cli.delete_medication(medication_id)
               if affected_users:
                  print("Affected Users:")
                  for user in affected_users:
                        print(f"Name: {user['FirstName']} {user['LastName']}")
               else:
                  print("No users were affected or an error occurred.")

            elif choice == 19:
               max_severity = cli.get_max_severity_of_diseases()
               if max_severity:
                  print(f"\nMaximum Severity of Diseases: {max_severity['MaxSeverity']}")
               else:
                  print("Error retrieving maximum severity.")

            elif choice == 20:
               ongoing_treatments = cli.get_total_ongoing_treatments()
               if ongoing_treatments:
                  print(f"\nTotal Ongoing Treatments: {ongoing_treatments['TotalOngoingTreatments']}")
               else:
                  print("Error retrieving ongoing treatments.")

            elif choice == 0:
                  print("Exiting...")
                  cli.close_connection()
                  break;

            else:
                print("Invalid option, please try again.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
