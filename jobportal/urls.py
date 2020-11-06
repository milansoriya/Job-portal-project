from django.urls import path,include
from . import views
from .views import JobseekerListView,jobListView

urlpatterns = [
   path("home",views.home,name='home'),
   path("Company_home",views.Company_home,name='Company_home'),
   path("AddJob",views.AddJob,name='AddJob'),
   path("UserProfile",views.UserProfile,name='UserProfile'),
   path("Company_profile",views.Company_profile,name='Company_profile'),
   path("Company_jobApplications",views.Company_jobApplications,name='Company_jobApplications'),
   path("UserjobApplications",views.UserjobApplications,name='UserjobApplications'),
   path("UserDetail/<int:id>",views.UserDetail,name='UserDetail'),
   path('jobs/<int:id>', views.JobDetailsView, name='jobs-detail'),
   path('jobList/', jobListView.as_view(), name='jobList'),
   path('JobseekerList/', JobseekerListView.as_view(), name='JobseekerList'),
   path("deleteRequest/<int:id>",views.deleteRequest,name='deleteRequest'),
   path("deleteApplication/<int:id>",views.deleteApplication,name='deleteApplication'),
   path("sendmail/<int:id>",views.sendmail,name='sendmail'),
   path("download_csv",views.download_csv,name='download_csv'),
   path("user_download_csv",views.user_download_csv,name='user_download_csv'),
   path("jobFilter",views.jobFilter,name='jobFilter'),
   path("jobseekerFilter",views.jobseekerFilter,name='jobseekerFilter'),
   path("sendOneMail/<int:id>",views.sendOneMail,name='sendOneMail'),
   path("sendAllMail",views.sendAllMail,name='sendAllMail'),
   path("EditUserProfile",views.EditUserProfile,name='EditUserProfile'),
   path("EditCompany_profile",views.EditCompany_profile,name='EditCompany_profile'),
   path("posted_job",views.posted_job,name='posted_job'),
   path("Edit_job",views.Edit_job,name='Edit_job'),
   path("addintolist/<int:id>",views.addintolist,name="addintolist"),
   path("interestList",views.interestList,name="interestList"),
   path("removeFromList/<int:id>",views.removeFromList,name="removeFromList"),
   path("download_list",views.download_list,name="download_list"),
   path("auto_complete", views.auto_complete, name='auto_complete'),
   path("about",views.about,name='about'),
   path("about1",views.about1,name='about1')
   
]
