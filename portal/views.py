from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import auth,User
from django.contrib import messages
from .forms import NewVehicleForm,rule_engineForm,Update_serviceForm,Update_odo_readingForm
from .models import NewVehicle,rule_engine
from datetime import *
import datetime
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth.decorators import login_required
import re

@never_cache
def home(request):
    if request.user.is_authenticated:
        return redirect('portal')
    return render(request,'home.html')


@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def login(request):
    if request.user.is_authenticated:
        return redirect('portal')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if not username:
            messages.info(request,"Username cant be empty")
            return redirect('login')
        if not password:
            messages.info(request,"Password cannot be empty")
            return redirect('login')
        if user is not None:
            auth.login(request,user)
            return redirect('portal')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def register(request):
    if request.user.is_authenticated:
        return redirect('portal')
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        if not username:
            messages.info(request, "Username cant be empty")
            return redirect('register')
        if not password1:
            messages.info(request, "Password cant be empty")
            return redirect('register')
        if not password2:
            messages.info(request, "Password  cant be empty")
            return redirect('register')
        if password1 == password2:
            if(User.objects.filter(username=username).exists()):
                messages.info(request,"Username already taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1)
                user.save()
                messages.info(request,"User Created")
                return redirect('login')
        else:
            messages.info(request,"Password Mismatch")
            return redirect('register')
    else:
        return render(request,'register.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def logout(request):
    auth.logout(request)
    return redirect('home')

@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
@login_required(login_url='home')
def portal(request):
    return render(request,'portal.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
@login_required(login_url='home')
def vehicle_create_view(request):  # vehicle registration view
    form = NewVehicleForm()
    context = {'form': form}
    if request.method == 'POST':  # if the user pressed submit button
        Register_No = request.POST['Register_No']  # store all the form data in variables
        Invoice_Date = request.POST['Invoice_Date']
        Previous_Service_Odo = request.POST['Previous_Service_Odo']
        Previous_Service_Date = request.POST['Previous_Service_Date']
        Current_Odo = request.POST['Current_Odo']
        if NewVehicle.objects.filter(
                Register_No=Register_No).exists():  # check if the vehicle is present in database and if present show message
            messages.info(request, "Vehicle already exists")
            return redirect('vehicle_create')
        if not isValidVehicleNumberPlate(Register_No):  # if the user entered invalid input
            messages.info(request, "Please Enter Valid Register Number")
            return redirect('vehicle_create')
        try:
            dateObject_invioce = datetime.datetime.strptime(Invoice_Date, '%Y-%m-%d')
            if dateObject_invioce > datetime.datetime.now():  # if the Date is less than Todays date then show message
                messages.info(request, "Date Should be less than Todays date")
                return redirect('vehicle_create')
        except ValueError:
            messages.info(request, "Incorrect date format, should be YYYY-MM-DD")
            return redirect('vehicle_create')
        try:
            dateObject_service = datetime.datetime.strptime(Previous_Service_Date, '%Y-%m-%d')
            if dateObject_service > datetime.datetime.now():  # if the Date is less than Todays date then show message
                messages.info(request, "Date Should be less than Todays date")
                return redirect('vehicle_create')
            if dateObject_invioce > dateObject_service:  # if Previous Service Date less than Invioce date then show message
                messages.info(request, "Previous Service Date Should be less than Invioce date")
                return redirect('vehicle_create')
        except ValueError:
            messages.info(request, "Incorrect data format, should be YYYY-MM-DD")
            return redirect('vehicle_create')
        if Previous_Service_Odo > Current_Odo:  # if Previous Service Odo less than or equal to Current Odo show message
            messages.info(request, "Previous Service Odo should be less than or equal to Current Odo")
            return redirect('vehicle_create')
        form = NewVehicleForm(request.POST)
        if form.is_valid():  # if the all the data is valid then store it in table
            form.save()
            messages.info(request, "Vehicle Saved Successfully")
            return redirect('vehicle_create')  # Add here

    return render(request, 'new_vehicle.html', context)  # add here


@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
@login_required(login_url='home')
def rule_engine_view(request):
    form = rule_engineForm()
    context = {'form': form}
    if request.method == 'POST':  # if the user pressed submit button
        projected_odo = request.POST['projected_odo']  # store all the form data in variables
        projected_days = request.POST['projected_days']
        buffer_odo = request.POST['buffer_odo']
        buffer_days = request.POST['buffer_days']
        print(projected_odo, buffer_odo, projected_days, buffer_days)
        if projected_odo < buffer_odo:  # if projected odois  more than to Buffer Odo then show message
            messages.info(request, "projected odo should be more than to Buffer Odo")
            return redirect('rule_engine')
        if projected_days[0] == '-' or buffer_days[0] == '-':  # if days entered in negative then show message
            messages.info(request, "days can not be negative")
            return redirect('rule_engine')
        form = rule_engineForm(request.POST)
        if form.is_valid():  # if the form is valid
            Bike_Name = request.POST['Bike_Name']
            Service_Count = request.POST['Service_Count']
            data = rule_engine.objects.filter(Bike_Name=Bike_Name,
                                              Service_Count=Service_Count)  # access the data row in a variable with the same bike name and service count
            for i in data:
                i.delete()  # delete the row if present
            form.save()  # save the row in table
            messages.info(request,"Updated successfully")
            return redirect('rule_engine')
    return render(request, 'rule_engine.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
@login_required(login_url='home')
def service_bikes(request):  # list for servicing bikes
    bike_details = NewVehicle.objects.all()  # storing all the bike details in variable
    bikes_to_be_serviced = apply_rules(bike_details)  # function call to get only servicing bikes
    outer = []
    # here bikes_to_be_serviced will return the list of lists with 5 datas in each list
    #  bikes_to_be_serviced will return row of bike to be serviced,due service date,remaining days ,remaing kms,due service odo
    for data in bikes_to_be_serviced:  # accesing each bike details
        if data[2] < 0 or data[
            3] < 0:  # if the remaining days or remaining kms any one of it is negative then store color as red
            color = "background-color:#FF0000"
        else:
            color = "background-color:#FFFFFF"
        k = {  # here we are creating a dictionary of all the values to be dislayed
            'Bike_Name': data[0].Bike_Name,
            'Register_No': data[0].Register_No,
            'due_service_date': data[1],
            'remaining_days': data[2],
            'remaining_kms': data[3],
            'due_service_odo': data[4],
            'color': color
        }
        outer.append(k)  # We store each dictionary to list

    return render(request, 'service_bikes.html', {'list': outer})


def apply_rules(bike_details):  # in this function we extract required data of both vehicle table and rule table
    bikes_to_be_serviced = []
    for row in bike_details:  # here we are going through each row
        if row.Service_Count < 3:  # if the service count is less than 3 we will check the  rule table and store the data in variable
            rules = rule_engine.objects.filter(Bike_Name=row.Bike_Name, Service_Count=row.Service_Count)
        else:
            rules = rule_engine.objects.filter(Bike_Name=row.Bike_Name,
                                               Service_Count=3)  # if the service count is 3 or more we will consider the rules of the 3rd service count as we assumed after 3 it will be static
        rules_data = {}
        for rule in rules:  # we are going throuh each rows which contains that rule there will be only one rule for the perticular bike and service count
            rules_data = {  # storing all the row data in dictionary
                'projected_days': convert_to_days(rule.projected_days),
                'projected_odo': rule.projected_odo,
                'buffer_days': convert_to_days(rule.buffer_days),
                'buffer_odo': rule.buffer_odo
            }

        bike_detail = {  # here we store the all required data of bike table
            'Invoice_Date': row.Invoice_Date,
            'Previous_Service_Odo': row.Previous_Service_Odo,
            'Previous_Service_Date': row.Previous_Service_Date,
            'Current_Odo': row.Current_Odo
        }
        if rules_data == {}:  # if there is no rule for the perticular bike we skip the bike
            continue
        condtion = perform(rules_data, bike_detail)  # this function call is made to calculate and give boolian value
        if condtion == False:
            continue
        else:
            bikes_to_be_serviced.append([row, condtion[1], condtion[2], condtion[3],
                                         condtion[4]])  # if the function returns true we append it to list
    return bikes_to_be_serviced


# this function return bool value for row of bike to be serviced,due service date,remaining days ,remaing kms,due service odo
def perform(rules_data, bike_detail):
    notifiction_from_date = bike_detail['Previous_Service_Date'] + timedelta(rules_data['projected_days'] - rules_data[
        'buffer_days'])  # here we calculate the date for the notifications to start
    notifiction_to_date = bike_detail['Previous_Service_Date'] + timedelta(
        rules_data['projected_days'])  # here we calculate the date for the vehicle to be serviced
    notifiction_from_odo = bike_detail['Previous_Service_Odo'] + rules_data['projected_odo'] - rules_data[
        'buffer_odo']  # here we calculate the odo for the notifications to start
    notifiction_to_odo = bike_detail['Previous_Service_Odo'] + rules_data[
        'projected_odo']  # here we calculate the odo for the vehicle to be serviced
    Current_Odo = bike_detail['Current_Odo']  # store the curreent odo in variable
    Current_Date = date.today()  # store the current date
    odo_condition = ((
                                 Current_Odo >= notifiction_from_odo and Current_Odo <= notifiction_to_odo) or Current_Odo >= notifiction_to_odo)  # here we check for the odo condition if the current odo is more than notifications to start odo reading then it stores true
    date_condtion = ((
                                 Current_Date >= notifiction_from_date and Current_Date <= notifiction_to_date) or Current_Date >= notifiction_to_date)  # here we check for the dae condition if the current date is more than notifications to start date then it stores true
    if odo_condition or date_condtion:  # if any of the condition satisfies we run the block of code
        due_days = notifiction_to_date - Current_Date  # here we calculate the days left to service the bike
        due_odo = notifiction_to_odo - Current_Odo  # here we calculate the kms left to service the bike
        return [True, notifiction_to_date, due_days.days, due_odo,
                notifiction_to_odo]  # here we return the list of values if the condition satisfies
    else:
        return False  # it returns false the bike does not needs to be serviced


# this function is used to convert string[days,months and years] to days
def convert_to_days(raw):
    if isinstance(raw, int):
        return raw
    s = ""
    for i in raw:
        if i.isnumeric():
            s += i
    s = int(s)
    if "day" in raw:
        s = s
    if "month" in raw:
        s = s * 30
    if "year" in raw:
        s = s * 365
    return s


# this function is to validate the vehicle rgister number
def isValidVehicleNumberPlate(str):  #

    regex = "^[A-Z]{2}[\\s-]{0,1}[0-9]{2}[\\s-]{0,1}[A-Z]{1,2}[\\s-]{0,1}[0-9]{4}$"  # this is regex for vehicle register number

    p = re.compile(regex)  # we use regex to evaluate the string

    if (str == None):
        return False

    if (re.search(p, str)):  # here we check the string with the regex
        return True
    else:
        return False


# Naveen




@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
@login_required(login_url='home')
def update(request):                                                                                                    #Service Update
    if request.method == 'POST':                                                                                        #to valid the method
        form = Update_serviceForm(request.POST)

        if form.is_valid():
            Register_No = form.cleaned_data['Register_No']
            current_odo = form.cleaned_data['current_odo']
            Service_completion_date = form.cleaned_data['Service_completion_date']
            try:
                if not Register_No:                                                                                     #if not register number show message
                    messages.info(request,"Register_No cant be empty")
                    return redirect('update_service')
                vehicle = NewVehicle.objects.get(Register_No=Register_No)
                if current_odo < vehicle.Current_Odo:                                                                   #to validate the current odo should not be less than last current odo
                    messages.info(request,"your entered odo should not be less then last time serviced odo")
                    return redirect('update_service')
                vehicle.Previous_Service_Odo = current_odo
                Service_completed_date = date.today()
                if Service_completion_date > date.today():                                                              #to check date is valid or not
                    messages.info(request,"the enterd date should be less than toady's date")
                    return redirect('update_service')
                if Service_completion_date < vehicle.Previous_Service_Date:                                             #to compare last service date to current date
                    messages.info(request,"your entered odo should not be less then last time serviced date")
                    return redirect('update_service')
                vehicle.Previous_Service_Date = Service_completion_date
                vehicle.Previous_Service_Date = Service_completed_date
                vehicle.Current_Odo = current_odo
                vehicle.Service_Count +=1                                                                               #to update sevice count by 1 after upadted
                vehicle.save()
                messages.info(request,"Service Details Updated successfully")
                return redirect('portal')

            except NewVehicle.DoesNotExist:
                messages.info(request, "Invalid Register Number")
                return redirect('update_odo_reading')
    else:
        form = Update_serviceForm()
    return render(request, 'update_service.html', {'form': form})




@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
@login_required(login_url='home')
def servicedue(request):                                                                                                #service due check
    if request.method == 'GET':
        return render(request, 'service_due_check.html')
    if request.method == 'POST':
        register_no = request.POST['register_no']

        try:
            register_no = request.POST.get('register_no')
            if not register_no:
                    messages.info(request,"Register_No can't be empty")
                    return redirect('servicedue')
            vehicle = NewVehicle.objects.get(Register_No=register_no)
            if vehicle.Service_Count>3:                                                                                 #to check service count
                try:
                    rule=rule_engine.objects.get(Bike_Name=vehicle.Bike_Name,Service_Count=3)
                except:
                    messages.info(request,"Rules for this model doesnot exist")
                    return redirect('servicedue')
            else:
                try:
                    rule=rule_engine.objects.get(Bike_Name=vehicle.Bike_Name,Service_Count=vehicle.Service_Count)
                except:
                    messages.info(request, "Rules for this model doesnot exist")
                    return redirect('servicedue')

            current_odo = vehicle.Current_Odo
            current_date = date.today()
            next_service_odo = vehicle.Previous_Service_Odo + rule.projected_odo                                        #formula for giving notification to the user
            buffer_odo = rule.buffer_odo
            if (next_service_odo-current_odo) <= buffer_odo:                                                            #to check the current odo is reches to next service odo and next service date
                odo_msg = 'Your vehicle needs service  because your reaching to your next srvice KM of :'
            else:
                odo_msg = 'Your vehicle does not need a service  but do service  your bike before reches srvice KM of :'
            next_service_date = vehicle.Previous_Service_Date + timedelta(days=convert_to_days(rule.projected_days))                #coverted days into date and added to the date
            buffer_date = timedelta(days=convert_to_days(rule.buffer_days))
            if (next_service_date-current_date) <= buffer_date:                                                         #to check the current date is reches to next service odo and next service date
                date_msg = "Your vehicle needs a service because your reches to your  vehicle service date of :"
            else:
                date_msg = "Your vehicle does not need a service but do service before reaching to the this date :"
        except NewVehicle.DoesNotExist:                                                                                 #to check registration number valid or not
                messages.info(request, "Invalid Register Number")
                return redirect('servicedue')
    return render(request, 'service_due_check.html',{'vehicle': vehicle,'odo_msg': odo_msg,'date_msg': date_msg,'next_service_odo':next_service_odo,'next_service_date':next_service_date})













@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
@login_required(login_url='home')
def check(request):                                                                                                     #update odo meter
    if request.method == 'POST':
        form = Update_odo_readingForm(request.POST)

        if form.is_valid():                                                                                             #to confirm is valid
            Register_No = form.cleaned_data['Register_No']
            current_odo = form.cleaned_data['current_odo']
            try:
                if not Register_No:
                    messages.info(request,"Register_No cant be empty")
                    return redirect('check')
                data = NewVehicle.objects.get(Register_No=Register_No)
                if current_odo < data.Current_Odo:                                                                      #to check current odo condition
                    messages.info(request,"Entred odo should not be less than last saved value")
                    return redirect('check')
                data.Current_Odo = current_odo                                                                          #to make entered odo as current odo also
                data.save()
                messages.info(request,"Odo Updated successfully")                                                       #to show message of data is saved
                return redirect('check')
            except NewVehicle.DoesNotExist:                                                                             #to show message if vehicle not available
                messages.info(request, "Invalid Register Number")
                return redirect('check')
    else:
        form = Update_odo_readingForm()
    return render(request, 'update_odo_reading.html', {'form': form})
