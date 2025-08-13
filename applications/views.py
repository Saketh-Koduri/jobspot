from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Application
from .forms import ApplicationForm
from jobs.models import Job

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user is a job seeker
    if request.user.is_company:
        messages.error(request, "Companies cannot apply for jobs.")
        return redirect('job_detail', job_id=job_id)
    
    # Check if user has already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('job_detail', job_id=job_id)
    else:
        form = ApplicationForm()
    
    return render(request, 'applications/apply.html', {
        'form': form,
        'job': job
    })

@login_required
def my_applications(request):
    # Only job seekers can view their applications
    if request.user.is_company:
        return redirect('dashboard')
    
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'applications/my_applications.html', {
        'applications': applications
    })

@login_required
def applicants_list(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Only the company that posted the job can view applicants
    if job.company != request.user:
        messages.error(request, "You don't have permission to view this.")
        return redirect('job_list')
    
    applications = Application.objects.filter(job=job)
    return render(request, 'applications/applicants_list.html', {
        'job': job,
        'applications': applications
    })

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    # Only the company that posted the job can update status
    if application.job.company != request.user:
        messages.error(request, "You don't have permission to do this.")
        return redirect('job_list')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'reviewed', 'accepted', 'rejected']:
            application.status = status
            application.save()
            messages.success(request, f"Application status updated to {status}.")
        else:
            messages.error(request, "Invalid status.")
    
    return redirect('applicants_list', job_id=application.job.id)

@login_required 
def withdraw_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    if application.status != 'pending':
        messages.error(request, "You can only withdraw pending applications.")
        return redirect('my_applications')
    
    application.delete()
    messages.success(request, "Application withdrawn successfully.")
    return redirect('my_applications')