from openpyxl import load_workbook
import pandas as pd

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

def import_employees_from_excel(file_path):
    # Read data from Excel file
    df = pd.read_excel(file_path)

    # Process the data and return it
    return df.values.tolist()

def validate_employee_name(name, employee_data):
    # Validate uniqueness of employee name
    for data in employee_data:
        if data[1].lower() == name.lower():
            return False, "Employee name already exists. Please enter a different name."
    return True, ""

def create_employee(employee_data):
    # Function to create an employee object
    last_id = int(employee_data[-1][0]) if employee_data else 100010
    new_employee_id = str(last_id + 1)

    while True:
        name = input("Enter employee name: ")
        valid_name, name_error = validate_employee_name(name, employee_data)
        if valid_name:
            break
        else:
            print("Error:", name_error)

    department = input("Enter department: ")
    wage = float(input("Enter wage: "))
    tenure = int(input("Enter tenure: "))
    avg_hours_per_week = int(input("Enter average hours per week: "))
    return Employee(new_employee_id, name, department, wage, tenure, avg_hours_per_week)

def append_employee_to_excel(employee, file_path):
    # Load existing data from Excel
    df = pd.read_excel(file_path)

    # Append new employee data
    new_row = [employee.employee_id, employee.name, employee.department, employee.wage, employee.tenure, employee.avg_hours_per_week]
    df.loc[len(df)] = new_row

    # Write back to Excel
    df.to_excel(file_path, index=False)

def main():
    # Load existing employee data from Excel
    file_path = "employee_data.xlsx"
    employee_data = import_employees_from_excel(file_path)
    
    while True:
        try:
            # Prompt user for action choice
            action = input("Enter '1' to create a new employee, '2' to access existing data, or 'exit' to quit: ")

            # Check if the user wants to exit
            if action.lower() == 'exit':
                print("Exiting the program...")
                break
            
            if action == '1':
                # Create a new employee
                new_employee = create_employee(employee_data)

                # Add the new employee to the Excel file
                append_employee_to_excel(new_employee, file_path)
                print("Employee added successfully!")

            elif action == '2':
                # Prompt user to enter employee ID
                employee_id = input("Enter your employee ID (or 'exit' to quit): ")

                # Check if the user wants to exit
                if employee_id.lower() == 'exit':
                    print("Exiting the program...")
                    break
                
                # Validate employee ID
                if not employee_id.isdigit() or len(employee_id) != 6:
                    raise ValueError("Invalid employee ID. Please enter a 6-digit numeric ID.")

                # Find employee data in spreadsheet from entered employee ID
                employee_info = None
                for data in employee_data:
                    if str(data[0]) == employee_id:
                        employee_info = data
                        break
                if employee_info is None:
                    raise ValueError("Employee ID not found in records.")

                # Create an employee object with loaded data
                employee1 = Employee(*employee_info)

                # Create a schedule for the employee
                shift1 = Shift("8:00 AM", "12:00 PM")
                shift2 = Shift("1:00 PM", "5:00 PM")
                schedule = Schedule(employee1, [shift1, shift2])

                # Create a department
                department1 = Department("Mechanical", [employee1])

                # Create an employee dashboard
                dashboard = EmployeeDashboard(employee1)
                dashboard.display_information()

                # Check if the employee is a manager
                is_manager = True  # Assume the employee is a manager

                # Open management options if the user is a manager
                if is_manager:
                    manager_dashboard = ManagerDashboard(employee1)
                    manager_dashboard.open_management_options()

        except ValueError as ve:
            print("Error:", ve)

if __name__ == "__main__":
    main()
