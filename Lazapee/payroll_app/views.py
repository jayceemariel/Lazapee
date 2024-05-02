from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages

id =0
# Create your views here.
def dashboard(request,pk):
    global id
    d = get_object_or_404(Account, pk=pk)
    id = d.user
    return render(request, 'home_dashboard.html', {'d':d,'id':id})

def employee(request,pk):
    global id
    d = get_object_or_404(Account, pk=pk)
    id = d.user
    e = Employee.objects.all()
    return render(request, 'Content/Employee/employee_info.html', 
                  {'d': d, 
                   'id':id,
                   'employee': e})

def update_employee(request,pk,id):
    e = get_object_or_404(Employee, pk=pk)
    d = get_object_or_404(Account, user=id)  
    id = str(id)
    return render(request, 'Content/Employee/update_employee.html',
                  {'d':d,
                    'id':id,
                   'e': e})

def add_employee(request, id):
    d = get_object_or_404(Account,  user=id)
    id = str(id)
    
    if request.method == "POST":
        name = request.POST.get('name')
        id_num = request.POST.get('id_num')
        rate = request.POST.get('rate')
        allowance = request.POST.get('Allowance')
        if not allowance:
            allowance = None
        Employee.objects.create(name=name, id_number= id_num, rate=rate, allowance=allowance)
        return redirect(request, 'Content/Employee/employee_info.html',{'d': d, 'id':id})
   
    return render(request, 'Content/Employee/add_employee.html',{'d': d, 'id':id})




def pay_slip(request,pk):
    global id
    d = get_object_or_404(Account, pk=pk)
    id = d.user
    p = PaySlip.objects.all()
    e = Employee.objects.all()
    return render(request, 'Content/Pay_Slip/Pay-slip_info.html', 
                  {'d':d,
                  'id':id,
                   'payslip': p,
                   'employee': e,})


def view_payslip(request,pk, id):
    p =  get_object_or_404(PaySlip, pk=pk)
    d = get_object_or_404(Account, user=id)  
    id = str(id)


    return render(request, 'Content/Pay_Slip/view_PaySlip.html',
                  {'d':d,
                    'id':id,
                   'p': p})
  

# MANAGE ACCOUNT
def manage_account(request,pk):
    global id
    d = get_object_or_404(Account, pk=pk)
    id = d.user
    return render(request, 'Account/manage_account.html', {'d': d, 'id':id})

def delete_account(request, pk):
    d = get_object_or_404(Account, pk=pk)
    d.delete()
    return redirect('login_view')

def change_password(request,pk):
    if(request.method=="POST"):
        currentPW = request.POST.get('dpassword')
        newPW = request.POST.get('dnew_password')
        confirmNewPW = request.POST.get('dconfirm_new_password')

        if Account.objects.filter(password=currentPW).exists():
            for call_psswrd in Account.objects.values():
                if call_psswrd['password'] == currentPW:
                    called_psswrd = call_psswrd['password']
                    break

            #if they are the same the password input
            if newPW == confirmNewPW:
                    Account.objects.filter(pk=pk).update(password = newPW)
                    return redirect('manage_account',pk=pk)
            else: #this probably not working sir so pasensya
                error_message = "Password aren't the same" #
                d = get_object_or_404(Account, pk=pk)
                #when wrong should display the error mesage
                return render(request, 'Account/change_password.html', {'d': d, 'error_message': error_message})
        else: #this probably not working sir so pasensya
            error_message = "Incorrect Current Password" #
            d = get_object_or_404(Account, pk=pk)
            #when wrong should display the error mesage
            return render(request, 'Account/change_password.html', {'d': d, 'error_message': error_message})
   
    else: 
        d = get_object_or_404(Account, pk=pk)
        return render(request, 'Account/change_password.html',{'d': d})


def login(request): 
    if(request.method =="POST"):
        usrname = request.POST.get('username')
        passwrd = request.POST.get('password')

        if Account.objects.filter(user=usrname).exists():
            for call_psswrd in Account.objects.values():
                if call_psswrd['user'] == usrname:
                    called_psswrd = call_psswrd['password']
                    break

            if called_psswrd == passwrd:
                pk = Account.objects.get(user=usrname).pk     # Retrieve the pk of the user account
                return employee(request, pk)
            else:
                error_message = 'Invalid login'
                return render(request, 'base_login.html', {'error_message': error_message})
  
        else:
            error_message = 'Invalid login'
            return render(request, 'base_login.html', {'error_message': error_message})
    else:

        return render(request, 'base_login.html')


def signup(request):
    if(request.method =="POST"):
        usrname = request.POST.get('username')
        passwrd = request.POST.get('password')

         # Error Statements
        if Account.objects.filter(user=usrname).exists():
            error_message = 'Account already exists'
            return render(request, 'Account/account_signup.html', {'error_message':  error_message})
        
        if not usrname:
            error_message = 'Username is required'
            return render(request, 'Account/account_signup.html', {'error_message': error_message})
        
        if not passwrd:
            error_message_pss = 'Password is required'
            return render(request, 'Account/account_signup.html', {'error_message_pss': error_message_pss})
        
        #Creates the Account once all the error statements have been passed
        Account.objects.create(user=usrname, password = passwrd)
        messages.success(request, 'Account created successfully')
        return redirect('Login') #goes to logIn once everything is submitted
    else: 
        return render(request, 'Account/account_signup.html')