from django.db import models

# Create your models here.
JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)

class User_Employee(models.Model):
   
    e_first_name=models.CharField(max_length=100)
    e_last_name=models.CharField(max_length=100)
    e_username=models.CharField(max_length=100)
    e_password=models.CharField(max_length=100)
    e_email=models.CharField(max_length=100)
    e_mobileno=models.CharField(max_length=10)
    e_add1=models.CharField(max_length=100)
    e_city=models.CharField(max_length=100)
    e_state=models.CharField(max_length=100)
    e_country=models.CharField(max_length=100)
    e_qualification=models.CharField(max_length=100)
    e_current_role=models.CharField(max_length=100)
    e_jobType=models.CharField(choices=JOB_TYPE, max_length=10)
    e_experience=models.IntegerField() 
    e_image=models.ImageField(upload_to='pics/employee')
    e_resume=models.FileField(upload_to='resumes')
    e_sort_description=models.TextField()

class User_Employeer(models.Model):
   
    c_name=models.CharField(max_length=100)
    c_full_description=models.TextField()
    c_logo=models.ImageField(upload_to='pics/employeer')
    c_username=models.CharField(max_length=100)
    c_password=models.CharField(max_length=100)
    c_add1=models.CharField(max_length=100)
    c_city=models.CharField(max_length=100)
    c_state=models.CharField(max_length=100)
    c_country=models.CharField(max_length=100)
    c_contact=models.CharField(max_length=10)
    c_email=models.CharField(max_length=100)
    c_website=models.CharField(max_length=100)