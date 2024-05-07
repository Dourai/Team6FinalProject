from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    employee_id = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        employee_id = cleaned_data.get('employee_id')
        password = cleaned_data.get('password')

        print(employee_id, password, 'AAAAAAAAA')
        if not employee_id:
            raise ValidationError('Employee id is required')

        if not password:
            raise ValidationError('Incorrect password')
