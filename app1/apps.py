
from django.apps import AppConfig
import os

class MyAppConfig(AppConfig):
    name = 'app1'
    verbose_name = 'Your Application'
    _classifier = None

    @property
    def classifier(self):
        if self._classifier is None:
            from tensorflow.keras.models import load_model
            # Assuming you've moved your model to be within your project structure
            model_path = os.path.join(os.path.dirname(__file__), 'D:\VS Scripts\RecycleSystem\myproject\model', 'model70%.h5')
            self._classifier = load_model(model_path)
        return self._classifier

    def ready(self):
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from .models import Profile
        from django.contrib.auth.models import User

        @receiver(post_save, sender=User)
        def create_or_update_user_profile(sender, instance, created, **kwargs):
            Profile.objects.get_or_create(user=instance)
            # Assuming the Profile model has logic to handle updates appropriately

