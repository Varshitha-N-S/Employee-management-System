from django.shortcuts import get_object_or_404, redirect, render, HttpResponse

from emp_app.forms import EmployeeForm
from .models import Employee, Department, Role
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate,login as auth_login



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')  # Redirect to 'index' after successful login
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')
    
# Create your views here.

def index(request):
    return render(request, 'index.html')


# def all_emp(request):
#     emps = Employee.objects.all()
#     context = {
#         'emps': emps
#     }
#     print(context)
#     return render(request, 'view_all_emp.html', context)

def all_emp(request):
    emps = Employee.objects.all()  # Get all employee records
    context = {
        'emps': emps  # Pass the employee records to the template
    }
    print(context)  # Optional: For debugging purposes
    return render(request, 'view_all_emp.html', context)  # Render the template with the context



# def add_emp(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         salary = int(request.POST['salary'])
#         bonus = int(request.POST['bonus'])
#         phone = int(request.POST['phone'])
#         dept = request.POST['dept']
#         role = request.POST['role']
#         new_emp = Employee(first_name= first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id = dept, role_id = role, hire_date = datetime.now())
#         new_emp.save()
#         return HttpResponse('Employee added Successfully')
#     elif request.method=='GET':
#         return render(request, 'add_emp.html')
#     else:
#         return HttpResponse("An Exception Occured! Employee Has Not Been Added")



def add_emp(request):
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            salary = int(request.POST['salary'])
            bonus = int(request.POST['bonus'])
            phone = int(request.POST['phone'])
            dept = request.POST['dept']
            role = request.POST['role']
            image = request.FILES.get('image')  # Handle the uploaded image file

            # Create and save the new employee
            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                bonus=bonus,
                phone=phone,
                dept_id=dept,
                role_id=role,
                hire_date=datetime.now(),
                image=image  # Save the image
            )
            new_emp.save()
            return HttpResponse('Employee added successfully!')
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    elif request.method == 'GET':
        # Optional: you can pass departments and roles to the template
        departments = Department.objects.all()
        roles = Role.objects.all()
        return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})
    else:
        return HttpResponse("An unexpected error occurred.")

# def remove_emp(request, emp_id = 0):
#     emps = Employee.objects.all()
#     context = {
#         'emps': emps
#     }
#     print(context)
#     if emp_id:
#         try:
#             emp_to_be_removed = Employee.objects.get(id=emp_id)
#             emp_to_be_removed.delete()
#             return HttpResponse("Employee Removed Successfully")
#         except:
#             return HttpResponse("Please Enter A Valid EMP ID")
#     emps = Employee.objects.all()
#     context = {
#         'emps': emps
#     }
#     return render(request, 'remove_emp.html',context)


from django.http import HttpResponse
from django.shortcuts import render
from .models import Employee

def remove_emp(request, emp_id=0):
    # Fetch all employees to display in the table
    emps = Employee.objects.all()
    
    # Check if an employee ID is provided and remove that employee
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except Employee.DoesNotExist:
            return HttpResponse("Please Enter A Valid EMP ID")

    # Pass the employee list to the template context
    context = {
        'emps': emps
    }
    
    return render(request, 'remove_emp.html', context)


def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps': emps
        }
        return render(request, 'view_all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')
    

def edit_emp(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=emp)
        if form.is_valid():
            form.save()
            return redirect('view_all_emp')  # Redirect to the employee list view
    else:
        form = EmployeeForm(instance=emp)

    context = {
        'form': form,
        'emp': emp,
    }

    return render(request, 'edit_emp.html', context)