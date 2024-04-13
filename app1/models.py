
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=(('generator', 'Generator'), ('recycler', 'Recycler')))
    # Assume email is already part of the User model, so we only add role here

    def __str__(self):
        return f"{self.user.username}'s profile"

class RecyclerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recycler_profile')
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100) # Consider using GeoDjango for real location fields
    
    def __str__(self):
        # Return the company name when the RecyclerProfile instance is printed or called
        return self.company_name

class GeneratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='generator_profile')
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)  # Same note on GeoDjango
    
    def __str__(self):
        return self.company_name 
    
class Appointment(models.Model):
    generator_name = models.ForeignKey(GeneratorProfile, on_delete=models.CASCADE, related_name='appointments')
    recycler_name = models.ForeignKey(RecyclerProfile, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True, null=True)
    #email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.generator_name.user.username} to {self.recycler_name.user.username} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"

    
class AppointmentMessage(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message by {self.author.username} on {self.created_at}"
    

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    expiry_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Subscription for {self.user.username}"    

class Payment(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paypal_order_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.paypal_order_id} by {self.payer.username}"


    

