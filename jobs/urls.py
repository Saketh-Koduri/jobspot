from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),  # /jobs/ - All jobs listing
    path('<int:job_id>/', views.job_detail, name='job_detail'),  # /jobs/1/ - Job detail
    path('create/', views.create_job, name='create_job'),  # /jobs/create/ - Post new job
    path('my/', views.my_jobs, name='my_jobs'),  # /jobs/my/ - Company's jobs
    path('<int:pk>/edit/', views.edit_job, name='edit_job'),  # /jobs/1/edit/ - Edit job
    path('<int:pk>/delete/', views.delete_job, name='delete_job'),  # /jobs/1/delete/ - Delete job
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.job_list, name='job_list'),
#     path('job/<int:pk>/edit/', views.edit_job, name='edit_job'),
#      path('job/<int:pk>/delete/', views.delete_job, name='delete_job'),  #
#     path('<int:job_id>/', views.job_detail, name='job_detail'),
#     path('create/', views.create_job, name='create_job'),
#     path('my/', views.my_jobs, name='my_jobs'),
#    ]
