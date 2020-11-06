from django.contrib import admin
from .models import Job,JobApplication,JobQualification,JobSeekerList
# Register your models here.
admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(JobQualification)
admin.site.register(JobSeekerList)