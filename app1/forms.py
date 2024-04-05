from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import RecyclerProfile, GeneratorProfile, Appointment

class RecyclerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        help_text='Required. Inform a valid email address.',
        widget=forms.TextInput(attrs={'style': 'width: 75%;','placeholder': 'Email'})
    )
    company_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'style': 'width: 75%;','placeholder': 'Company Name'})
    )
    location = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'style': 'width: 75%;','placeholder': 'Location'})
    )
    # Override the username field
    username = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 75%;', 'placeholder': 'Username'}))

    # Override the password1 and password2 fields
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width: 75%;', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width: 75%;', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ('username', 'company_name', 'email', 'location', 'password1', 'password2')

        
        
class GeneratorSignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        help_text='Required. Inform a valid email address.',
        widget=forms.TextInput(attrs={'style': 'width: 75%;','placeholder': 'Email'})
    )
    company_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'style': 'width: 75%;','placeholder': 'Company Name'})
    )
    location = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'style': 'width: 75%;','placeholder': 'Location'})
    )
    username = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 75%;', 'placeholder': 'Username'}))

    # Override the password1 and password2 fields
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width: 75%;', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'width: 75%;', 'placeholder': 'Confirm Password'})
    )
    # Adding role field for demonstration, though it might not be used in this form

    class Meta(UserCreationForm.Meta):
        model = User
        # Ensure 'email' field is part of the form fields
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        # Email field is already handled by the base User model, no need to set it explicitly here if included in fields
        if commit:
            user.save()
            # Create the generator profile with additional information
            GeneratorProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                location=self.cleaned_data['location']
            )
        return user
    

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['generator_name', 'recycler_name', 'appointment_date', 'details']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
