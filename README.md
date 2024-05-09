# Team6FinalProject
Here you will find all information and files relevant to Team 6's Staff Management System.

# What is the Staff Management System?
The Staff Management System is a web application that allows administrations to manage their staff. Managers can add, edit, and delete staff members, as well as view their staff members' information. Staff members can also view their own information, clock in and out, and change their own information: name, password.

- Administrators can:
  - Add, edit, and delete staff members
  - View staff members' information

- Staff members can:
  - View their own information
  - Clock in and out
  - Change their own information: name, password

# How to run the Staff Management System
1. Clone the repository
2. Navigate to the `staff_management` project directory
3. Run the following command to create virtual environment:
   ```
   python -m venv myenv
   ```
4. Run the following command to activate the virtual environment:
   ```
    source ./myenv/bin/activate (Linux)
    .\myenv\Scripts\activate (Windows)
   ```
4. Run the following command to create a superuser: (optional - you will be asked for: username, name, password, ternue, department, wage, and avg_hours_per_week)
   ```
   python manage.py createsuperuser
   ```
5. Run the following command to run the server:
   ```
    python manage.py runserver
   ```
6. Open a web browser and navigate to `http://127.0.0.1:8000/`
7. Log in with the superuser credentials you created in step 4, or use these default credentials:

  **Superuser:**
   - Username: admin
   - Password: admin

  **Staff:**
   - Username: staff
   - Password: staff

# Technologies
  - Python 3.8.5
  - Django
  - SQLite

# Demo site
http://thinguyen.pythonanywhere.com/
