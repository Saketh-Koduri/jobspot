from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import CustomUserCreationForm,LoginForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def register_user(request):
    if request.user.is_authenticated:   # <--- Add this at the top
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            print(f"User created: {user}")
            login(request,user)
            return redirect('dashboard')
    else:
        form=CustomUserCreationForm()
    return render(request,'users/register.html',{'form':form})

def login_user(request):
    if request.user.is_authenticated:   # <--- Add this at the top
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  # Use request as the first arg
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            form.add_error(None, "Invalid username or password.")  # Safe to use here
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    from jobs.models import Job  # import here if not already globally imported

    # Count job stats
    total_jobs = Job.objects.count()
    total_companies = CustomUser.objects.filter(is_company=True).count()

    # Filter featured jobs (customize as needed)
    featured_jobs = Job.objects.order_by('-created_at')[:6]

    # Optional: filters from GET query
    search_query = request.GET.get('search', '')
    location_query = request.GET.get('location', '')
    job_type_filter = request.GET.get('job_type', '')

    # Job type choices (adjust as per your model)
    job_type_choices = Job.JOB_TYPE_CHOICES if hasattr(Job, 'JOB_TYPE_CHOICES') else []

    context = {
        'role': 'company' if request.user.is_company else 'seeker',
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'featured_jobs': featured_jobs,
        'search_query': search_query,
        'location_query': location_query,
        'job_type_filter': job_type_filter,
        'job_type_choices': job_type_choices,
    }

    return render(request, 'users/dashboard.html', context)

# @login_required
# def dashboard(request):
#     if request.user.is_company:
#         return render(request,'users/dashboard.html',{'role':'company'})
#     else:
#         return render(request,'users/dashboard.html',{'role':'seeker'})
