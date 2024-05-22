from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from decimal import Decimal
from django.contrib import messages

un =0
# Create your views here.

def employee(request,pk):
    global un
    d = get_object_or_404(Account, pk=pk)
    un = d.user
    e = Employee.objects.all()
    return render(request, 'Content/Employee/employee_info.html', 
                  {'d': d, 
                   'id':un,
                   'employee': e})

def update_employee(request, pk, id):
    e = get_object_or_404(Employee, pk=pk)
    d = get_object_or_404(Account, user=id)
    id = str(id)

    if request.method == "POST":
        name = request.POST.get('name')
        rate = request.POST.get('rate')
        allowance = request.POST.get('Allowance')

        # update attributes
        e.name = name
        e.rate = rate
        e.allowance = allowance
        e.save()

        return redirect('employee', pk=d.pk)

    else:
        return render(request, 'Content/Employee/update_employee.html', {'d':d, 'id':id, 'e': e})

def add_employee(request, id):
    d = get_object_or_404(Account,  user=id)
   
    id = str(id)
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            id_num = request.POST.get('id_num')
            rate = request.POST.get('rate')
            allowance = request.POST.get('Allowance')

            if not allowance:
                allowance = 0
            
            Employee.objects.create(name=name, id_number= id_num, rate=rate, allowance=allowance, overtime_pay=0)
            return redirect('employee', pk=d.pk)
    except:
        '''
            Source for messages:
            The messages framework. (n.d.). Django. Retrieved from:
            https://docs.djangoproject.com/en/5.0/ref/contrib/messages.
        '''
        return render(request, 'Content/Employee/add_employee.html',{'d': d, 'id':id, 'message': 'ID Number taken. Please input a new ID Number.'})
    
    return render(request, 'Content/Employee/add_employee.html',{'d': d, 'id':id})

def delete_employee(request, id, pk):
    Employee.objects.filter(pk=pk).delete()
    return redirect('employee', pk=id)

def delete_all_employees(request, id): #deletes all employees for fun
    d = get_object_or_404(Account, user=id)
    Employee.objects.all().delete()
    return redirect('employee', pk=d.pk)

def overtime(request, id, pk):
    if request.method == 'POST':
        try:
            e = get_object_or_404(Employee, pk=pk)
            d = get_object_or_404(Account, pk=id)
            ot_hours = float(request.POST.get('hours'))

            rate = e.getRate()
            pay = (rate / 160) * 1.5 * ot_hours
            
            e.overtime_pay += pay
            e.save()
            return redirect('employee', pk=id)

        except Exception as e:
            return render(request, 'Content/Employee/employee_info.html', 
                  {'d': d, 
                   'id':d.getUsername, 'employee': Employee.objects.all, 'message': 'Please enter a number.'})

    else:
        return redirect('employee', pk=id)

def reset_overtime(request, id, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.resetOvertime()
    return redirect('employee', pk=id)

def pay_slip(request, pk):
    global un
    d = get_object_or_404(Account, pk=pk)
    p = PaySlip.objects.all()
    e = Employee.objects.all()
    idnums = [p.id_number for p in PaySlip.objects.all()]

    if (request.method == 'POST'):
        id_number = request.POST.get('idno')
        month = request.POST.get('month')
        year = request.POST.get('year')
        pay_cycle = request.POST.get('pay_cycle')
        
        
        # convert pay_cycle to int since it's a string in form
        pay_cycle = int(pay_cycle)

        if id_number == "All": #Generate payslip for all employees
            if PaySlip.objects.filter(month=month, year=year,pay_cycle=pay_cycle).exists(): #if payslip matching criteria already exists:
                return render(request, 'Content/Pay_Slip/Pay-slip_info.html',
                          {'d': d, 'id': d.user, 'payslip': p, 'employee': e, 'message': 'Those payslips have already been generated.'})
            else:
                for employee in e:

                    # given deductions
                    pag_ibig = 100
                    philhealth = employee.rate * 0.04
                    sss = employee.rate * 0.045

                    # if fields are none, set to zero
                    if employee.allowance is None:
                        employee.allowance = 0

                    if employee.overtime_pay is None:
                        employee.overtime_pay = 0

                    # cycle 1: pag-ibig
                    if pay_cycle == 1:
                        basecomp = ((employee.rate/2) + employee.allowance + employee.overtime_pay - pag_ibig)
                        # date_range based on cycle
                        date_range = "1-15"

                    # cycle 2: philhealth & sss
                    elif pay_cycle == 2:
                        basecomp = ((employee.rate/2) + employee.allowance + employee.overtime_pay - philhealth - sss)
                        # check for february date range
                        if month == "February":
                            date_range = "16-28"
                        else:
                            date_range = "16-30"

                    # tax and total
                    tax = basecomp * 0.2
                    total = basecomp - tax

                    # generate payslip with all fields
                    PaySlip.objects.create(id_number=employee, month = month, date_range = date_range, year = year, pay_cycle = pay_cycle, rate=employee.rate, earnings_allowance = employee.allowance, deductions_tax = tax, deductions_health = philhealth, pag_ibig = pag_ibig, sss = sss, overtime = employee.overtime_pay, total_pay = total)

                    # reset overtime pay after generating payslip
                    employee.resetOvertime()

                return render(request, 'Content/Pay_Slip/Pay-slip_info.html',
                            {'d': d, 'id': d.user, 'payslip': p, 'employee': e, 'message': 'Generated Payslips for all employees.'})

        
        # get employee corresponding to given id_n
        employee = Employee.objects.get(id_number = id_number)
        if employee in idnums and PaySlip.objects.filter(month=month, year=year,pay_cycle=pay_cycle).exists():      
            return render(request, 'Content/Pay_Slip/Pay-slip_info.html', {'d':d, 'id':d.user, 'payslip': p, 'employee': e, 'message': 'Payslip already exists!'})
        
        else: # payslip doesnt exist yet
            
            # given deductions
            pag_ibig = 100
            philhealth = employee.rate * 0.04
            sss = employee.rate * 0.045

            # if fields are none, set to zero
            if employee.allowance is None:
                employee.allowance = 0

            if employee.overtime_pay is None:
                employee.overtime_pay = 0

            # cycle 1: pag-ibig
            if pay_cycle == 1:
                basecomp = ((employee.rate/2) + employee.allowance + employee.overtime_pay - pag_ibig)
                # date_range based on cycle
                date_range = "1-15"

            # cycle 2: philhealth & sss
            elif pay_cycle == 2:
                basecomp = ((employee.rate/2) + employee.allowance + employee.overtime_pay - philhealth - sss)
                # check for february date range
                if month == "February":
                    date_range = "16-28"
                else:
                    date_range = "16-30"

            # tax and total
            tax = basecomp * 0.2
            total = basecomp - tax

            # generate payslip with all fields
            PaySlip.objects.create(id_number = Employee.objects.get(id_number = id_number), month = month, date_range = date_range, year = year, pay_cycle = pay_cycle, rate=employee.rate, earnings_allowance = employee.allowance, deductions_tax = tax, deductions_health = philhealth, pag_ibig = pag_ibig, sss = sss, overtime = employee.overtime_pay, total_pay = total)

            # reset overtime pay after generating payslip
            employee.resetOvertime()

            return render(request, 'Content/Pay_Slip/Pay-slip_info.html', {'d': d, 'id': d.user, 'payslip': p, 'employee': e, 'message': 'Payslip generated for {}, ID Number: {}'.format(employee.getName(), employee.getID())})
    
    else:
        return render(request, 'Content/Pay_Slip/Pay-slip_info.html', {'d': d, 'id': d.user, 'payslip': p, 'employee': e,})
    
def delete_payslips(request, id): #deletes all payslips for fun
    d = get_object_or_404(Account, user=id)
    PaySlip.objects.all().delete()
    p = PaySlip.objects.all()
    e = Employee.objects.all()
    return render(request, 'Content/Pay_Slip/Pay-slip_info.html', {'d': d, 'id': un, 'payslip': p, 'employee': e,})

def view_payslip(request,pk, id):
    p =  get_object_or_404(PaySlip, pk=pk)
    d = get_object_or_404(Account, user=id)
    id = str(id)

    # since rate is divided by half in computations
    halfrate = p.rate/2

    gross = halfrate + p.earnings_allowance + p.overtime

    # values of rows to display deductions on the table (sidenote: this is absolutely horrible but it works :sob:)
    deduct_one_one = ''
    deduct_one_two = ''
    deduct_two_one = ''
    deduct_two_two = ''

    # table display for cycle 1
    if p.pay_cycle == 1:
        deductions = p.deductions_tax + p.pag_ibig
        deduct_one_one = "PAG-IBIG"
        deduct_one_two = str(p.pag_ibig)

    # ditto, cycle 2
    elif p.pay_cycle == 2:
        deductions = p.deductions_tax + p.deductions_health + p.sss
        deduct_one_one = "PHILHEALTH"
        deduct_one_two = str(p.deductions_health)
        deduct_two_one = "SSS"
        deduct_two_two = str(p.sss)

    return render(request, 'Content/Pay_Slip/view_PaySlip.html', {'d':d, 'id': id, 'p': p, 'hr': halfrate, 'gross': gross, 'ddct': deductions, 'dd11': deduct_one_one, 'dd12': deduct_one_two, 'dd21': deduct_two_one, 'dd22': deduct_two_two,})

# MANAGE ACCOUNT
def manage_account(request,pk):
    global id
    d = get_object_or_404(Account, pk=pk)
    id = d.user
    return render(request, 'Account/manage_account.html', {'d': d, 'id':id})



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
    
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    try:
        Account.objects.filter(pk=pk).delete()
        return redirect('Login')
    except Exception as e:
        return render(request, 'Account/manage_account.html', {'d': account, 'id':account.user})