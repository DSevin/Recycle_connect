
# Register your models here.
from django.contrib import admin
from .models import RecyclerProfile, GeneratorProfile, Appointment, Subscription, Payment

admin.site.register(RecyclerProfile)
admin.site.register(GeneratorProfile)
admin.site.register(Appointment)
admin.site.register(Subscription)
admin.site.register(Payment)