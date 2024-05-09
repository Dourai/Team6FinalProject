from django import forms
from django.core.exceptions import ValidationError
from .models import Employee

# This form is used to validate the login form
class LoginForm(forms.Form):
    employee_id = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        employee_id = cleaned_data.get('employee_id')
        password = cleaned_data.get('password')

        if not employee_id:
            raise ValidationError('Employee id is required')

        if not password:
            raise ValidationError('Incorrect password')


# This form is used to update the employee's name
class EmployeeNameUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name']

    # Validate the name before saving it
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == '':
            raise ValidationError('This field cannot be blank.')
        return name

# This form is used to update the employee's password
class EmployeePasswordUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['password']

    # Validate the password before saving it
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 5:
                raise ValidationError('Password must be at least 5 characters long.')
            if ' ' in password:
                raise ValidationError('Password cannot contain whitespace.')
        else:
            # Remove password from the cleaned data if it's blank
            self.cleaned_data.pop('password', None)
        return password
