from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage
from .models import User_Employee,User_Employeer
# Create your views here.
def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        login_as=request.POST.get('login_as')
       
        if login_as == 'employee':
            try:
                user = User_Employee.objects.get(e_username=username)
                if user.e_password==password:
                    request.session['user_id']=user.id
                    request.session['user_name']=user.e_first_name
                    return redirect("home")
                else:
                    messages.info(request,'Invalid credentials')
                    return redirect('/')
            except:
                messages.info(request,'Invalid credentials')
                return redirect('/') 
        elif login_as == 'employer':
            try:
                user = User_Employeer.objects.get(c_username=username)
                if user.c_password==password:
                    request.session['company_id']=user.id
                    request.session['company_name']=user.c_name
                    return redirect("Company_home")
                else:
                    messages.info(request,'Invalid credentials')
                    return redirect('/')
            except:
                messages.info(request,'Invalid credentials')
                return redirect('/')
    else:
        return render(request,'login.html')

def Employeer_registration(request):
    if request.method == 'POST':
        c_name=request.POST.get('c_name')
        c_email=request.POST.get('c_email')
        c_contact=request.POST.get('c_contact')
        c_username=request.POST.get('c_username')
        c_website=request.POST.get('c_website')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        c_add1=request.POST.get('c_add1')
        c_city=request.POST.get('c_city')
        c_state=request.POST.get('c_state')
        c_country=request.POST.get('c_country')
        c_full_description=request.POST.get('c_full_description')
        c_logo=request.FILES['c_logo']

        
        if password1 == password2 :
            if User_Employeer.objects.filter(c_username=c_username).exists():
                messages.info(request,'Username Taken')
                return redirect('Employeer_registration')
            elif User_Employeer.objects.filter(c_email=c_email).exists():
                messages.info(request,'Email Taken')
                return redirect('Employeer_registration')
            else:     
                fs = FileSystemStorage(base_url="pics/employeer",location="media/pics/employeer")
                filename = fs.save(c_logo.name, c_logo)
                                              
                user=User_Employeer(c_name=c_name,
                                   c_username=c_username,
                                   c_password=password1,
                                   c_email=c_email,
                                   c_contact=c_contact,
                                   c_add1=c_add1,
                                   c_city=c_city,
                                   c_state=c_state,
                                   c_country=c_country,
                                   c_website=c_website,
                                   c_logo=fs.url(filename),
                                   c_full_description=c_full_description )
                user.save()
                print('company created')
                return redirect('/')

        else:
            messages.info(request,'password not matching..')
            return redirect('Employeer_registration') 
        return redirect('/')       
    else:
        return render(request,'Employeer_registration.html')

def Employee_registration(request):
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        mobile_no=request.POST.get('mobile_no')
        username=request.POST.get('username')
        qualification=request.POST.get('qualification')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        house_no=request.POST.get('house_no')
        city=request.POST.get('city')
        state=request.POST.get('state')
        country=request.POST.get('country')
        s_description=request.POST.get('s_description')
        user_image=request.FILES['user_image']
        user_resume=request.FILES['user_resume']

        
        if password1 == password2 :
            if User_Employee.objects.filter(e_username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('Employee_registration')
            elif User_Employee.objects.filter(e_email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('Employee_registration')
            else:     
                fs = FileSystemStorage(base_url="pics/employee",location="media/pics/employee")
                filename = fs.save(user_image.name, user_image)
                fs1 = FileSystemStorage(base_url="resumes",location="media/resumes")
                filename1 = fs1.save(user_resume.name, user_resume)
               # print(filename+" "+filename1)                              
                user=User_Employee(e_first_name=first_name,
                                   e_last_name=last_name,
                                   e_username=username,
                                   e_password=password1,
                                   e_email=email,
                                   e_mobileno=mobile_no,
                                   e_add1=house_no,
                                   e_city=city,
                                   e_state=state,
                                   e_country=country,
                                   e_qualification=qualification,
                                   e_image=fs.url(filename),
                                   e_resume=fs1.url(filename1),
                                   e_sort_description=s_description )
                user.save()
                #print('user created')
                return redirect('/')

        else:
            messages.info(request,'password not matching..')
            return redirect('Employee_registration') 
        return redirect('/')       
    else:
        return render(request,'Employee_registration.html')


def Company_logout(request):
    del request.session['company_id']
    del request.session['company_name']
    return redirect('/')

def User_logout(request):
    del request.session['user_id']
    del request.session['user_name']
    return redirect('/')
