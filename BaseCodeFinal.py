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

class Schedule:
    def __init__(self, employee, shifts):
        # Initialize schedule with associated employee and shifts
        self.employee = employee
        self.shifts = shifts

    def add_shift(self, shift):
        # Add a new shift to the schedule
        self.shifts.append(shift)

    def remove_shift(self, shift):
        # Remove a shift from the schedule
        self.shifts.remove(shift)

    def update_shift(self, shift, new_shift):
        # Update an existing shift in the schedule
        index = self.shifts.index(shift)
        self.shifts[index] = new_shift

class Shift:
    def __init__(self, start_time, end_time):
        # Initialize shift with start and end times
        self.start_time = start_time
        self.end_time = end_time

class Department:
    def __init__(self, name, employees):
        # Initialize department with name and employees
        self.name = name
        self.employees = employees

    def add_employee(self, employee):
        # Add an employee to the department
        self.employees.append(employee)

    def remove_employee(self, employee):
        # Remove an employee from the department
        self.employees.remove(employee)

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

def fetch_employee_by_id(employee_id):
    conn = sqlite3.connect(DB_FILE)
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

def main():
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
            employee = fetch_employee_by_id(employee_id)

            if employee:
                # Display information for the fetched employee
                print("Employee Name:", employee.name)
                print("Employee ID:", employee.employee_id)
                print("Department:", employee.department)
                print("Wage:", employee.wage)
                print("Tenure:", employee.tenure)
                print("Average Hours Per Week:", employee.avg_hours_per_week)
                print()

                # Check if the employee is in the Manager department
                if employee.department == "Manager":
                    # Create an employee dashboard
                    dashboard = EmployeeDashboard(employee)
                    dashboard.display_information()

                    # Open management options if the user is a manager
                    manager_dashboard = ManagerDashboard(employee)
                    manager_dashboard.open_management_options()

            else:
                print("Employee not found.")

            # Create a schedule for the employee
            shift1 = Shift("8:00 AM", "12:00 PM")
            shift2 = Shift("1:00 PM", "5:00 PM")
            schedule = Schedule(employee, [shift1, shift2])

            # Create a department
            department1 = Department("Mechanical", [employee])

        except ValueError as ve:
            print("Error:", ve)

if __name__ == "__main__":
    main()
