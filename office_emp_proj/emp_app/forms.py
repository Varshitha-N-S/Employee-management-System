from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'salary', 'bonus', 'phone', 'dept', 'role', 'image']  # Adjust according to the fields in your model
