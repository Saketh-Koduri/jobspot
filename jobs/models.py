from django.db import models
from django.conf import settings
from users.models import CustomUser

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('REMOTE', 'Remote'),
        # Add more types if needed
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    company = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_company': True})
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
