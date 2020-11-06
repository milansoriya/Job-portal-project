from django.db import models
from accounts.models import User_Employeer,User_Employee
# Create your models here.
JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)

class Job(models.Model):

    j_title=models.CharField(max_length=100)
    j_location=models.CharField(max_length=100)
    j_c_id=models.ForeignKey(User_Employeer,on_delete=models.CASCADE)
    j_experience=models.IntegerField()
    j_type = models.CharField(choices=JOB_TYPE, max_length=10)
    j_sort_description=models.TextField()
    j_salary=models.CharField(max_length=100)

class JobQualification(models.Model):

    j_id=models.ForeignKey(Job,on_delete=models.CASCADE)
    jq_qualification=models.TextField()

class JobApplication(models.Model):
    j_id=models.ForeignKey(Job,on_delete=models.CASCADE)
    e_id=models.ForeignKey(User_Employee,on_delete=models.CASCADE)

class JobSeekerList(models.Model):
    e_id=models.ForeignKey(User_Employee,on_delete=models.CASCADE)
    c_id=models.ForeignKey(User_Employeer,on_delete=models.CASCADE)