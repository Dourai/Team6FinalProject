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

# Main function to run the program
def main():
    while True:
        # Prompt user to enter employee ID
        employee_id = input("Enter your employee ID (or 'exit' to quit): ")

        # Check if the user wants to exit
        if employee_id.lower() == 'exit':
            print("Exiting the program...")
            break

        # Create an employee based on entered employee ID
        employee1 = Employee(employee_id, "John Doe", "Mechanical", 15.50, 2, 40)

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

if __name__ == "__main__":
    main()