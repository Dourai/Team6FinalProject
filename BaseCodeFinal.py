import sqlite3

# Define database file path
DB_FILE = 'employee_database.db'

class Employee:
    def __init__(self, employee_id, name, department, wage, tenure, avg_hours_per_week):
        # Initialize employee attributes
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.wage = wage
        self.tenure = tenure
        self.avg_hours_per_week = avg_hours_per_week

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def fetch_employee_by_id(self, employee_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Get employee from the database by employee_id
        c.execute("SELECT * FROM Employee WHERE employee_id = ?", (employee_id,))
        employee_data = c.fetchone()

        conn.close()

        # If employee with the given ID is found, create an Employee object
        if employee_data:
            return Employee(*employee_data)
        else:
            return None

class EmployeeDashboard:
    def __init__(self, employee):
        # Initialize employee dashboard with associated employee
        self.employee = employee

    def display_information(self):
        # Display basic information about the employee
        print("Employee Name:", self.employee.name)
        print("Employee ID:", self.employee.employee_id)
        print("Department:", self.employee.department)
        print("Wage:", self.employee.wage)
        print("Tenure:", self.employee.tenure)
        print("Average Hours Per Week:", self.employee.avg_hours_per_week)

class ManagerDashboard(EmployeeDashboard):
    def __init__(self, employee):
        # Initialize manager dashboard with associated employee
        super().__init__(employee)

    def open_management_options(self):
        # Open management options menu for the manager
        print("Management options menu opened")

def main():
    db_manager = DatabaseManager(DB_FILE)

    while True:
        try:
            # Prompt user to enter employee ID
            employee_id = input("Enter your employee ID (or 'exit' to quit): ")

            # Check if the user wants to exit
            if employee_id.lower() == 'exit':
                print("Exiting the program...")
                break
            
            # Validate employee ID
            if not employee_id.isdigit() or len(employee_id) != 6:
                raise ValueError("Invalid employee ID. Please enter a 6-digit numeric ID.")

            # Fetch employee by ID
            employee = db_manager.fetch_employee_by_id(employee_id)

            if employee:
                # Display information for the fetched employee
                dashboard = EmployeeDashboard(employee)
                dashboard.display_information()

                # Check if the employee is in the Manager department
                if employee.department == "Manager":
                    # Open management options if the user is a manager
                    manager_dashboard = ManagerDashboard(employee)
                    manager_dashboard.open_management_options()

            else:
                print("Employee not found.")

        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            break

        except ValueError as ve:
            print("Error:", ve)

        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()

