from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('applicants/<int:job_id>/', views.applicants_list, name='applicants_list'),
    path('update-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('withdraw/<int:application_id>/', views.withdraw_application, name='withdraw_application'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_job')

]