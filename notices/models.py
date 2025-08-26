from django.db import models
from django.contrib.auth import get_user_model
from complaints.models import Category, Municipality, Ward, Status
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class TrainingStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g. Available, Expired

    def __str__(self):
        return self.name
    

class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    training_status = models.ForeignKey(TrainingStatus, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='training/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(null=True, blank=True)  

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Set default expiry date if not provided (e.g., 10 days after creation)
        if not self.expiry_date:
            self.expiry_date = timezone.now() + timedelta(days=10)  # or 15 days
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expiry_date
    
class TrainingRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='trainingregistrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.training.title + ' - ' + self.user.username
    
    
class Vacancy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    vacancy_status = models.ForeignKey(TrainingStatus, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(null=True, blank=True)  
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = timezone.now() + timedelta(days=10) 
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expiry_date
    
class VacancyRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='vacancyregistrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Vacancy.title + ' - ' + self.user.username

class Information(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        return self.title