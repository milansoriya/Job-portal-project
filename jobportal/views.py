from django.shortcuts import render,redirect
from .models import Job,JobQualification,JobApplication
from accounts.models import User_Employeer,User_Employee
from django.views.generic import  ListView
from django.contrib import messages
from django.core.mail import send_mail
from telusko import settings
import csv
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

# Create your views here.

def jobFilter(request):
    if request.session.get('user_id'):
        jobType=request.GET.get('jobType')
        Experience=request.GET.get('Experience')
        Salary=request.GET.get('Salary')
    
        if Experience=='all':
            min=-1
            max=-1
        elif Experience=='0to5':
            min=0
            max=5
        elif Experience=='5to10':
            min=5
            max=10
        elif Experience=='10to15':
            min=10
            max=15
        elif Experience=='15to20':
            min=15
            max=20

        if Salary=='all':
            mins=-1
            maxs=-1
        elif Salary=='0to3':
            mins=0 
            maxs=300000
        elif Salary=='3to6':
            mins=300000
            maxs=600000
        elif Salary=='6to9':
            mins=600000
            maxs=900000
        elif Salary=='9plus':
            mins=900000
            maxs=999999900000

        if 'title' in request.session:
            title=request.session['title']
      
        if 'location' in request.session:
            location=request.session['location']
    
        if title!="" and location!="":
            jobs=Job.objects.filter(j_title=title,j_location=location)
        elif title!="" and location=="":
            jobs=Job.objects.filter(j_title=title)
        elif title=="" and location!="":
            jobs=Job.objects.filter(j_location=location)
        else:
            jobs=Job.objects.all()

        jobs1=[]
        for job in jobs:
            if jobType=='0':
                jobs1.append(job)
            if job.j_type==jobType:
                jobs1.append(job)
    
    
        jobs2=[]
        for job in jobs1:
            if Experience=='all':
                jobs2.append(job)
            if job.j_experience >=min and job.j_experience<=max:
                jobs2.append(job)
    
        jobs3=[]
        for job in jobs2:
            if Salary=='all':
                jobs3.append(job)
            if int(job.j_salary) >=mins and int(job.j_salary)<=maxs:
                jobs3.append(job)
    

        fjob=jobs3
        job_company=[]         
        for job in fjob:
            company=User_Employeer.objects.get(id=job.j_c_id_id)
            job_company.append([job,company]) 
        context={'object_list':job_company}
        return render(request,'jobList.html',context)
    else:
        return redirect('/')

class jobListView(ListView):
    model = Job
    template_name = 'jobList.html'

    def get_queryset(self): 
        q=""
        q1=""
        q = self.request.GET.get('title')
        q1 = self.request.GET.get('location')  
        self.request.session['title']=q
        self.request.session['location']=q1
        if q!="" and q1!="":
            jobs=Job.objects.filter(j_title=q,j_location=q1)
        elif q!="" and q1=="":
            jobs=Job.objects.filter(j_title=q)
        elif q=="" and q1!="":
            jobs=Job.objects.filter(j_location=q1)
        else:
            jobs=Job.objects.all()
        job_company=[]
        for job in jobs:
            company=User_Employeer.objects.get(id=job.j_c_id_id)
            job_company.append([job,company])      
        return job_company


class JobseekerListView(ListView):
    model = User_Employee
    template_name = 'JobseekerList.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company=User_Employeer.objects.get(id=self.request.session.get('company_id'))
        jobs=Job.objects.filter(j_c_id_id=company)
        context['jobs'] = jobs

        return context
    
    def get_queryset(self): 
        q=""
        q1=""
        q = self.request.GET.get('Qualification')
        q1 = self.request.GET.get('location')  
        self.request.session['Qualification']=q
        self.request.session['location']=q1
        if q!="" and q1!="":
            users=User_Employee.objects.filter(e_qualification=q,e_city=q1)
        elif q!="" and q1=="":
            users=User_Employee.objects.filter(e_qualification=q)
        elif q=="" and q1!="":
            users=User_Employee.objects.filter(e_city=q1) 
        else:
            users=User_Employee.objects.all()
        return users

def sendOneMail(request,id):
    if request.session.get('company_id'):
        Qualification=request.session['Qualification']
        location=request.session['location']
        if Qualification!="" and location!="":
            users=User_Employee.objects.filter(e_qualification=Qualification,e_city=location)
        elif Qualification!="" and location=="":
            users=User_Employee.objects.filter(e_qualification=Qualification)
        elif Qualification=="" and location!="":
            users=User_Employee.objects.filter(e_city=location) 
        else:
            users=User_Employee.objects.all()

        company=request.session['company_name']
        user=User_Employee.objects.get(id=id)
        #for user in users:
        subject = "From JOB PORTAL"
        msg = "Dear "+user.e_first_name+",\n  Greeting from "+company+"\n\n  Congratulations!! We are glad to inform you that you are shortlisted for interview process."
        to = user.e_email
        res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
        #print(res)
        context={'object_list':users}
        return render(request,"JobseekerList.html",context)
    else:
        return redirect('/')

def sendAllMail(request):
    if request.session.get('company_id'):
        Qualification=request.session['Qualification']
        location=request.session['location']
        jobtitle=request.POST.get('joblist')
        if Qualification!="" and location!="":
            users=User_Employee.objects.filter(e_qualification=Qualification,e_city=location)
        elif Qualification!="" and location=="":
            users=User_Employee.objects.filter(e_qualification=Qualification)
        elif Qualification=="" and location!="":
            users=User_Employee.objects.filter(e_city=location) 
        else:
            users=User_Employee.objects.all()

        company=request.session['company_name']
    
        for user in users:
            subject = "From JOB PORTAL"
            msg = "Dear "+user.e_first_name+",\n  Greeting from "+company+"\n\n  Congratulations!! We are glad to inform you that you are shortlisted for interview process for "+jobtitle
            to = user.e_email
            res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    
        company=User_Employeer.objects.get(id=request.session.get('company_id'))
        jobs=Job.objects.filter(j_c_id_id=company)
        
        context={'object_list':users,'jobs':jobs}
        return render(request,"JobseekerList.html",context)
    else:
        return redirect('/')
        
def home(request):
    if request.session.get('user_id'):
        j=Job.objects.all()[:6]
        jobs=[]
        user=User_Employee.objects.get(id=request.session.get('user_id'))
        for job in j:
            company=User_Employeer.objects.get(id=job.j_c_id_id)
            jobs.append([job,company])
        return render(request,"home.html",{'jobs': jobs,'user':user})
    else:
        return redirect('/')

def Company_home(request):
    if request.session.get('company_id'):
        j=User_Employee.objects.all()[:6]
        return render(request,"Company_home.html",{'jobs_seekers': j})
    else:
        return redirect('/')

def UserProfile(request):
    if request.session.get('user_id'):
        if request.method=="POST":
            user_image=request.FILES.get('user_image')
            user_resume=request.FILES.get('user_resume')

            user=User_Employee.objects.get(id=request.session.get('user_id'))
            
            if user_image:
                fs = FileSystemStorage(base_url="pics/employee",location="media/pics/employee")
                filename = fs.save(user_image.name, user_image)
                user.e_image=fs.url(filename)
            if user_resume:
                fs1 = FileSystemStorage(base_url="resumes",location="media/resumes")
                filename1 = fs1.save(user_resume.name, user_resume)
                user.e_resume=fs.url(filename1)

            user.e_first_name=request.POST.get('first_name')
            user.e_last_name=request.POST.get('last_name')
            user.e_email=request.POST.get('email')
            user.e_mobileno=request.POST.get('mobile_no')
            user.e_username=request.POST.get('username')
            user.e_qualification=request.POST.get('qualification')
            user.e_add1=request.POST.get('house_no')
            user.e_city=request.POST.get('city')
            user.e_state=request.POST.get('state')
            user.e_country=request.POST.get('country')
            user.save()
            return render(request,"UserProfile.html",{'user':user})
        else:
            user=User_Employee.objects.get(id=request.session.get('user_id'))
            return render(request,"UserProfile.html",{'user':user})
    else:
        return redirect('/')

def UserDetail(request,id):
    user=User_Employee.objects.get(id=id)
    return render(request,"UserDetail.html",{'user':user})

def JobDetailsView(request,id):
    if request.session.get('user_id'):
        job=Job.objects.get(id=id)
        company=User_Employeer.objects.get(id=job.j_c_id_id)
        qualification=JobQualification.objects.all().filter(j_id=id)

        if request.method=='POST':
            user=User_Employee.objects.get(id=request.session.get('user_id'))
            if JobApplication.objects.filter(j_id=job,e_id=user).exists():
                messages.info(request,"Already Applied")
                return render(request,"JobProfile.html",{'job':job,'company':company,'qualification':qualification})
            else:    
                application=JobApplication(j_id=job,e_id=user)
                application.save()
                messages.info(request,"Successfully Applied")
            return render(request,"JobProfile.html",{'job':job,'company':company,'qualification':qualification})
        else:
            return render(request,"JobProfile.html",{'job':job,'company':company,'qualification':qualification})
    else:
        return redirect('/')

def AddJob(request):
    if request.session.get('company_id'):
        if request.method == 'POST':
            j_title=request.POST.get('j_title')
            j_location=request.POST.get('j_location')
            j_salary=request.POST.get('j_salary')
            j_experience=request.POST.get('j_experience')
            j_type=request.POST.get('j_type')
            j_sort_description=request.POST.get('j_sort_description')
            j_c_id_id=request.session.get('company_id')
            #print(j_sort_description)
        
            if j_type=='Full Time':
                type=1
            elif j_type=='Part Time':
                type=2
            elif j_type=='Internship':
                type=3

            #print(type)
            job=Job(j_title=j_title,
                    j_location=j_location,
                    j_salary=j_salary,
                    j_experience=j_experience,
                    j_type=type,
                    j_sort_description=j_sort_description,
                    j_c_id_id=j_c_id_id)
        
            job.save()

            j_qualification=request.POST.get('j_qualification')

            qualifications=j_qualification.splitlines()
            #print(j_qualification)
            for q in qualifications:
                j_id=job.id
                jq_qualification=q
                qua=JobQualification(j_id=job,jq_qualification=jq_qualification)
                qua.save()
            #print('job added')
            return render(request,"AddJob.html")
        else:
            return render(request,"AddJob.html")
    else:
        return redirect('/')
def Company_profile(request):
    if request.session.get('company_id'):
        if request.method=="POST":
            company=User_Employeer.objects.get(id=request.session.get('company_id'))

            c_logo=request.FILES.get('c_logo')
            if c_logo:
                fs = FileSystemStorage(base_url="pics/employeer",location="media/pics/employeer")
                filename = fs.save(c_logo.name, c_logo)
        
            company.c_name=request.POST.get('c_name')
            company.c_email=request.POST.get('c_email')
            company.c_contact=request.POST.get('c_contact')
            company.c_username=request.POST.get('c_username')
            company.c_website=request.POST.get('c_website')
            company.c_add1=request.POST.get('c_add1')
            company.c_city=request.POST.get('c_city')
            company.c_state=request.POST.get('c_state')
            company.c_country=request.POST.get('c_country')
            company.save()
            return render(request,"Employeer/Company_profile.html",{'company':company})
        else:
            company=User_Employeer.objects.get(id=request.session.get('company_id'))
            return render(request,"Employeer/Company_profile.html",{'company':company})
    else:
        return redirect('/')

def Company_jobApplications(request):
    if request.session.get('company_id'):
        if request.method=='POST':
            company=User_Employeer.objects.get(id=request.session.get('company_id'))
            jobs=Job.objects.filter(j_c_id_id=company)
        
            job=Job.objects.get(j_title=request.POST.get('joblist'),j_c_id_id=company)
            request.session['selectedjob']=request.POST.get('joblist')
            jobapp=JobApplication.objects.filter(j_id_id=job)
            users=[]
            for app in jobapp:
                jobseeker=User_Employee.objects.get(id=app.e_id_id)
                #print(jobseeker)
                users.append(jobseeker)
            return render(request,"Employeer/Company_jobApplications.html",{'jobs':jobs,'users':users,'sj':job})  

        else:
            company=User_Employeer.objects.get(id=request.session.get('company_id'))
            jobs=Job.objects.filter(j_c_id_id=company)
            return render(request,"Employeer/Company_jobApplications.html",{'jobs':jobs})
    
    else:
        return redirect('/')

def deleteRequest(request,id):
    if request.session.get('company_id'):
        duser=User_Employee.objects.get(id=id)

        company=User_Employeer.objects.get(id=request.session.get('company_id'))
        jobs=Job.objects.filter(j_c_id_id=company)
        title=request.session.get('selectedjob')
        job=Job.objects.get(j_title=title,j_c_id_id=company)
    

        application=JobApplication.objects.get(e_id_id=duser,j_id_id=job)
        application.delete()

        jobapp=JobApplication.objects.filter(j_id_id=job)
        users=[]
        for app in jobapp:
            jobseeker=User_Employee.objects.get(id=app.e_id_id)
            users.append(jobseeker)
           
        return render(request,"Employeer/Company_jobApplications.html",{'jobs':jobs,'users':users,'sj':job})  
    else:
        return redirect('/')

def sendmail(request,id):
    if request.session.get('company_id'):
        suser=User_Employee.objects.get(id=id)

        company=User_Employeer.objects.get(id=request.session.get('company_id'))
        jobs=Job.objects.filter(j_c_id_id=company)
        title=request.session.get('selectedjob')
        job=Job.objects.get(j_title=title,j_c_id_id=company)

        subject = "JOB PORTAL"
        msg = "Congratulations you select for the interview process"
        to = suser.e_email
        res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])

        application=JobApplication.objects.get(e_id_id=suser,j_id_id=job)
        application.delete()

        jobapp=JobApplication.objects.filter(j_id_id=job)
        users=[]
        for app in jobapp:
            jobseeker=User_Employee.objects.get(id=app.e_id_id)
            users.append(jobseeker)
           
        return render(request,"Employeer/Company_jobApplications.html",{'jobs':jobs,'users':users,'sj':job})  
    else:
        return redirect('/')

def download_csv(request):
    if request.session.get('company_id'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Applications.csv"'

        writer = csv.writer(response)
        writer.writerow(['Sr. No.','Job Title','First Name','Last Name','User Name','Email','Mobile No.','Qualification','Address 1','City','State','Country'])

        company=User_Employeer.objects.get(id=request.session.get('company_id'))
        title=request.session.get('selectedjob')
        job=Job.objects.get(j_title=title,j_c_id_id=company)

        i=1
        jobapp=JobApplication.objects.filter(j_id_id=job)
        for app in jobapp:
            jobseeker=User_Employee.objects.get(id=app.e_id_id)
            writer.writerow([i,title,jobseeker.e_first_name,jobseeker.e_last_name,jobseeker.e_username,jobseeker.e_email,jobseeker.e_mobileno,jobseeker.e_qualification,jobseeker.e_add1,jobseeker.e_city,jobseeker.e_state,jobseeker.e_country])
            i=i+1
        return response
    else:
        return redirect('/')

def UserjobApplications(request):
    if request.session.get('user_id'):
        user=User_Employee.objects.get(id=request.session.get('user_id'))
        jobApp=JobApplication.objects.filter(e_id_id=user)
        jobs=[]
        for j in jobApp:
            job=Job.objects.get(id=j.j_id_id)
            company=User_Employeer.objects.get(id=job.j_c_id_id)
            jobs.append([job,company])
        #print(jobs)
        return render(request,'UserjobApplications.html',{'jobs':jobs})
    else:
        return redirect('/')

def deleteApplication(request,id):
    if request.session.get('usere_id'):
        job=Job.objects.get(id=id)
        duser=User_Employee.objects.get(id=request.session.get('user_id'))

        application=JobApplication.objects.get(e_id_id=duser,j_id_id=job)
        application.delete()

        user=User_Employee.objects.get(id=request.session.get('user_id'))
        jobApp=JobApplication.objects.filter(e_id_id=user)
        jobs=[]
        for j in jobApp:
            job=Job.objects.get(id=j.j_id_id)
            company=User_Employeer.objects.get(id=job.j_c_id_id)
            jobs.append([job,company])
        #print(jobs)
        return render(request,'UserjobApplications.html',{'jobs':jobs})
    else:
        return redirect('/')

def user_download_csv(request):
    if request.session.get('user_id'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Applications.csv"'

        writer = csv.writer(response)
        writer.writerow(['Sr. No.','Job Title','company'])

        user=User_Employee.objects.get(id=request.session.get('user_id'))
        jobApp=JobApplication.objects.filter(e_id_id=user)

        i=1
        for j in jobApp:
            job=Job.objects.get(id=j.j_id_id)
            company=User_Employeer.objects.get(id=job.j_c_id_id)
            writer.writerow([i,job.j_title,company.c_name])
            i=i+1
        return response
    else:
        return redirect('/')

def EditUserProfile(request):
    if request.session.get('user_id'):
        user=User_Employee.objects.get(id=request.session.get('user_id'))
        return render(request,"EditUserProfile.html",{'user':user})
    else:
        return redirect('/')

def EditCompany_profile(request):
    if request.session.get('company_id'):
        company=User_Employeer.objects.get(id=request.session.get('company_id'))
        return render(request,"Employeer/EditCompany_profile.html",{'company':company})
    else:
        return redirect('/')

def posted_job(request):
    if request.session.get('company_id'):
        if request.method=="POST":
            id=request.session.get('job_id')
            del request.session['job_id']
            job=Job.objects.get(id=id)
            job.j_title=request.POST.get('j_title')
            job.j_location=request.POST.get('j_location')
            job.j_salary=request.POST.get('j_salary')
            job.j_experience=request.POST.get('j_experience')
            job.j_sort_description=request.POST.get('j_sort_description')
           
            if request.POST.get('j_type')=='Full Time':
                job.j_type=1
            elif request.POST.get('j_type')=='Part Time':
                job.j_type=2
            elif request.POST.get('j_type')=='Internship':
                job.j_type=3
            
            job.save()

            j_qualification=request.POST.get('j_qualification')
            qualifications=j_qualification.splitlines()
            
            qual=JobQualification.objects.filter(j_id_id=id)
            for q in qual:
                q.delete()

            for q in qualifications:
                j_id=job.id
                jq_qualification=q
                qua=JobQualification(j_id=job,jq_qualification=jq_qualification)
                qua.save()

            company=User_Employeer.objects.get(id=request.session.get('company_id'))
            jobs=Job.objects.filter(j_c_id_id=company)
            return render(request,"Employeer/posted_job.html",{'jobs':jobs})
        else:
            company=User_Employeer.objects.get(id=request.session.get('company_id'))
            jobs=Job.objects.filter(j_c_id_id=company)
            return render(request,"Employeer/posted_job.html",{'jobs':jobs})
    else:
        return redirect('/')

def Edit_job(request):
    if request.session.get('company_id'):
        if request.method=="POST":
            company=User_Employeer.objects.get(id=request.session.get('company_id'))
            job=Job.objects.get(j_title=request.POST.get('joblist'),j_c_id_id=company)
            request.session['job_id']=job.id
            qual=JobQualification.objects.filter(j_id_id=job)
            qualification=""
            for q in qual:
                qualification=qualification+"\n"+q.jq_qualification
            return render(request,"Employeer/Edit_job.html",{'job':job ,'qualification':qualification})
        else:
            company=User_Employeer.objects.get(id=request.session.get('company_id'))
            jobs=Job.objects.filter(j_c_id_id=company)
            return render(request,"Employeer/posted_job.html",{'jobs':jobs})
    else:
        return redirect('/')