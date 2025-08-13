from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Job
from .forms import JobForm
from django.contrib import messages
from django.core.paginator import Paginator

# Homepage with featured jobs and search
def homepage(request):
    # Get search query
    search_query = request.GET.get('search', '')
    location_query = request.GET.get('location', '')
    job_type_filter = request.GET.get('job_type', '')
    
    # Start with all jobs
    jobs = Job.objects.all()
    
    # Apply filters
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if location_query:
        jobs = jobs.filter(location__icontains=location_query)
        
    if job_type_filter:
        jobs = jobs.filter(job_type=job_type_filter)
    
    # Get featured jobs (latest 6)
    featured_jobs = jobs.order_by('-created_at')[:6]
    
    # Get statistics for homepage
    total_jobs = Job.objects.count()
    total_companies = Job.objects.values('company').distinct().count()
    job_types = Job.objects.values('job_type').annotate(count=Count('job_type'))
    
    context = {
        'featured_jobs': featured_jobs,
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'job_types': job_types,
        'search_query': search_query,
        'location_query': location_query,
        'job_type_filter': job_type_filter,
        'job_type_choices': Job._meta.get_field('job_type').choices,
    }
    
    return render(request, 'jobs/homepage.html', context)

# Enhanced job list with search and pagination
def job_list(request):
    # Get search parameters
    search_query = request.GET.get('search', '')
    location_query = request.GET.get('location', '')
    job_type_filter = request.GET.get('job_type', '')
    
    # Start with all jobs
    jobs = Job.objects.all()
    
    # Apply filters
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(company__username__icontains=search_query)
        )
    
    if location_query:
        jobs = jobs.filter(location__icontains=location_query)
        
    if job_type_filter:
        jobs = jobs.filter(job_type=job_type_filter)
    
    # Order by latest
    jobs = jobs.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(jobs, 10)  # 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'location_query': location_query,
        'job_type_filter': job_type_filter,
        'job_type_choices': Job._meta.get_field('job_type').choices,
        'total_jobs': jobs.count(),
    }
    
    return render(request, 'jobs/job_list.html', context)

# Enhanced job details
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Get related jobs (same company or similar job type)
    related_jobs = Job.objects.filter(
        Q(company=job.company) | Q(job_type=job.job_type)
    ).exclude(id=job.id)[:3]
    
    # Check if user has already applied (if authenticated)
    has_applied = False
    if request.user.is_authenticated:
        from applications.models import Application
        has_applied = Application.objects.filter(
            job=job, 
            applicant=request.user
        ).exists()
    
    context = {
        'job': job,
        'related_jobs': related_jobs,
        'has_applied': has_applied,
    }
    
    return render(request, 'jobs/job_detail.html', context)

# Company can post a new job
@login_required
def create_job(request):
    if not request.user.is_company:
        messages.error(request, 'Only companies can post jobs.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('my_jobs')
    else:
        form = JobForm()
    return render(request, 'jobs/create_job.html', {'form': form})

# Company's posted jobs with statistics
@login_required
def my_jobs(request):
    if not request.user.is_company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
        
    jobs = Job.objects.filter(company=request.user).order_by('-created_at')
    
    # Get statistics
    from applications.models import Application
    total_jobs = jobs.count()
    total_applications = Application.objects.filter(job__company=request.user).count()
    pending_applications = Application.objects.filter(
        job__company=request.user, 
        status='pending'
    ).count()
    
    context = {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
    }
    
    return render(request, 'jobs/my_jobs.html', context)

# Company can edit a posted job
@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('my_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user)
    job_title = job.title
    job.delete()
    messages.success(request, f'Job "{job_title}" deleted successfully!')
    return redirect('my_jobs')

# applications/views.py
def apply_job(request, job_id):
    # your logic here
    pass

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Job
# from .forms import JobForm
# from django.contrib import messages
# # View all jobs (for seekers)
# def job_list(request):
#     jobs = Job.objects.all().order_by('-created_at')
#     return render(request, 'jobs/job_list.html', {'jobs': jobs})

# # Job details
# def job_detail(request, job_id):
#     job = get_object_or_404(Job, id=job_id)
#     return render(request, 'jobs/job_detail.html', {'job': job})

# # Company can post a new job
# @login_required
# def create_job(request):
#     if not request.user.is_company:
#         return redirect('dashboard')  # only companies can post

#     if request.method == 'POST':
#         form = JobForm(request.POST)
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.company = request.user
#             job.save()
#             return redirect('my_jobs')
#     else:
#         form = JobForm()
#     return render(request, 'jobs/create_job.html', {'form': form})

# # Company’s posted jobs
# @login_required
# def my_jobs(request):
#     jobs = Job.objects.filter(company=request.user)
#     return render(request, 'jobs/my_jobs.html', {'jobs': jobs})

# # Company can edit a posted job
# @login_required
# def edit_job(request, pk):
#     print("EDIT VIEW CALLED FOR PK:", pk)  # Add this
#     job = get_object_or_404(Job, pk=pk, company=request.user)
#     print("JOB FOUND:", job)
#     if request.method == 'POST':
#         form = JobForm(request.POST, instance=job)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Job updated successfully!')
#             return redirect('my_jobs')
#     else:
#         form = JobForm(instance=job)

#     return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

# @login_required
# def delete_job(request, pk):
#     job = get_object_or_404(Job, pk=pk, company=request.user)  # Ensure only the job's company can delete it
#     job.delete()
#     return redirect('my_jobs')  # Redirect back to the user's job list after deletion
