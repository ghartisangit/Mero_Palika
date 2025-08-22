from django.db import models
from django.contrib.auth import get_user_model
from complaints.models import Category, Municipality, Ward, Status

User = get_user_model()


class TrainingStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g. Available, Expired

    def __str__(self):
        return self.name
    

class RegisterStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g. Accepted, Pending

    def __str__(self):
        return self.name


class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True)
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
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    training_status = models.ForeignKey(TrainingStatus, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='training/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class TrainingRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='registrations')
    registration_status = models.ForeignKey(RegisterStatus, on_delete=models.SET_NULL, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.training.title + ' - ' + self.user.username
    
    
class Vacancy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    vacancy_status = models.ForeignKey(TrainingStatus, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='vacancy/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class VacancyRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='vacancyregistrations')
    VacancyRegistration_status = models.ForeignKey(RegisterStatus, on_delete=models.SET_NULL, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Vacancy.title + ' - ' + self.user.username

class Information(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        return self.title