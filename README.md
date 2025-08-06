# Medi-Fit Healthcare Management System

## Overview
Medi-Fit is a personalized healthcare management system designed to provide tailored medical solutions based on comprehensive patient profiles.

## Prerequisites
- Python 3.x
- PyMySQL
- MySQL Server

## Installation
1. Clone the repository
2. Install dependencies: `pip install pymysql`
3. Set up MySQL database using the provided schema
4. Update database connection details in the script

## Available Commands

### 1. **Retrieve Users by Blood Group**
- **Description:** Retrieves all users with a specified blood group.
- **Input:** Blood Group (default: 'O+')
- **Output:** List of users with their names and locations.

### 2. **Retrieve Users with Ongoing Treatments**
- **Description:** Retrieves all users who currently have ongoing treatments.
- **Output:** List of users with ongoing treatments.

### 3. **Retrieve MRI Test Reports**
- **Description:** Retrieves MRI test reports for users within a specified number of years.
- **Input:** Number of years (default: 1)
- **Output:** List of MRI test reports including user names and test times.

### 4. **Retrieve Users Location by Blood Group**
- **Description:** Retrieves the locations of users with a specified blood group.
- **Input:** Blood Group (default: 'A-')
- **Output:** List of users and their locations.

### 5. **Retrieve Allopathy Diseases**
- **Description:** Retrieves allopathy diseases from the database.
- **Output:** List of allopathy diseases.

### 6. **Search Users by Name Prefix**
- **Description:** Searches users by a name prefix.
- **Input:** Name prefix (default: 'Jo')
- **Output:** List of users with names starting with the specified prefix.

### 7. **Search Test Reports by Type**
- **Description:** Searches test reports by the test type (e.g., CT, MRI, etc.).
- **Input:** Test type (default: 'CT')
- **Output:** List of test reports of the specified type.

### 8. **Search Diseases by Symptom**
- **Description:** Searches diseases based on a symptom.
- **Input:** Symptom to search (default: 'cough')
- **Output:** List of diseases associated with the symptom.

### 9. **Calculate Comprehensive Health Metrics**
- **Description:** Calculates comprehensive health metrics such as average BMI, treatment expenses, etc.
- **Output:** Comprehensive health metrics (e.g., average BMI, total treatment expenses).

### 10. **Find Average BMI**
- **Description:** Calculates the average BMI for all users.
- **Output:** Average BMI value.

### 11. **Find Average Cancer Treatment Expense**
- **Description:** Calculates the average cancer treatment expense for all users.
- **Output:** Average cancer treatment expense.

### 12. **Analyze High Severity Treatments**
- **Description:** Analyzes high-severity treatments based on a severity threshold.
- **Input:** Severity threshold (default: 7)
- **Output:** Count of users with high-severity treatments.

### 13. **Analyze Allopathy Treatments**
- **Description:** Analyzes the number of patients undergoing allopathy treatments.
- **Output:** Number of patients with allopathy treatments.

### 14. **Insert New User**
- **Description:** Inserts a new user into the system.
- **Input:** User details (First Name, Last Name, Blood Group, etc.)
- **Output:** Confirmation of the new user ID.

### 15. **Insert New Disease**
- **Description:** Inserts a new disease into the system.
- **Input:** Disease details (Name, Severity, etc.)
- **Output:** Confirmation of the new disease ID.

### 16. **Update User Weight**
- **Description:** Updates the weight of a user and calculates the new BMI.
- **Input:** User ID, New weight (kg)
- **Output:** Updated BMI value.

### 17. **Update Treatment Status**
- **Description:** Updates the status of a user's treatment (e.g., Completed, Ongoing).
- **Input:** User ID, Treatment ID, New Treatment Status (default: 'Completed')
- **Output:** Confirmation of status update.

### 18. **Delete Medication**
- **Description:** Deletes medication from the database and identifies affected users.
- **Input:** Medication ID
- **Output:** List of affected users.

### 19. **Calculate Maximum Severity of Diseases**
- **Description:** Retrieves the maximum severity of all diseases.
- **Output:** Maximum severity value.

### 20. **Total Ongoing Treatments**
- **Description:** Retrieves the total number of ongoing treatments.
- **Output:** Total number of ongoing treatments.
