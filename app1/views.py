from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecyclerSignUpForm, GeneratorSignUpForm, AppointmentForm
from .models import RecyclerProfile, GeneratorProfile, Appointment, AppointmentMessage
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecyclerSignUpForm
from .models import RecyclerProfile, User
from django.contrib.auth.models import Group
from .models import Payment



# Create your views here.
from django.http import JsonResponse
from .apps import MyAppConfig

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.apps import apps
from .utils import preprocess_image, process_prediction  # Adjust this import based on your actual preprocessing function
from django.contrib.auth.models import Group

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests

import logging

logger = logging.getLogger(__name__)


# Example view for the homepage
def index(request):
    return render(request, 'index.html')

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image', None):
        image_file = request.FILES['image']
        
        # Basic validation to ensure the uploaded file is an image
        if not image_file.content_type.startswith('image/'):
            return render(request, 'upload.html', {'error': 'The uploaded file is not a valid image.'})
        
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)

        try:
            # Assuming 'preprocess_image' function is adapted to handle an InMemoryUploadedFile and returns correctly formatted image array
            processed_image = preprocess_image(image_file, target_size=(150, 150))
            
            classifier = apps.get_app_config('app1').classifier  # Ensure 'app1' matches your Django app's name where the model is loaded
            prediction = classifier.predict(processed_image)
            class_name = process_prediction(prediction)  # Implement this to translate prediction to class name

            # Save the result and URL in the session for retrieval in the next request
            request.session['classification_result'] = class_name
            request.session['uploaded_file_url'] = uploaded_file_url

        except Exception as e:
            # Handle exceptions, possibly logging them
            print(e)  # Consider using logging instead of print in a real project
            return render(request, 'upload.html', {'error': 'Error processing the uploaded image.'})

        # Redirect to the classification result page
        return redirect('classification_result')  # Ensure there is a URL named 'classification_result' in your urls.py

    # If not POST or no file is uploaded, render the upload form again
    return render(request, 'upload.html')

def classification_result(request):
    # Retrieve classification result and uploaded file URL from the session
    classification_result = request.session.get('classification_result', 'No classification made')
    uploaded_file_url = request.session.get('uploaded_file_url', '')

    return render(request, 'classification_result.html', {
        'uploaded_file_url': uploaded_file_url,
        'classification_result': classification_result,
    })

def recycler_list(request):
    recyclers = RecyclerProfile.objects.all()
    return render(request, 'recyclers_list.html', {'recyclers': recyclers})

def generator_list(request):
    generators = GeneratorProfile.objects.all()
    return render(request, 'generator_list.html', {'generators': generators})

import logging
from .forms import RecyclerSignUpForm

# Set up logging
logger = logging.getLogger(__name__)

def recycler_signup(request):
    if request.method == 'POST':
        form = RecyclerSignUpForm(request.POST)
        if form.is_valid():
            # Store form data in session temporarily
            request.session['recycler_signup_form_data'] = form.cleaned_data
            # Log the session data storage action
            logger.debug("Session data set for signup: %s", request.session.get('recycler_signup_form_data'))
            # Redirect to subscription page
            return redirect('subscription_page')
    else:
        form = RecyclerSignUpForm()
    return render(request, 'recycler_signup.html', {'form': form})



def subscription_page(request):
    # Render the subscription page with PayPal button
    # No change needed here unless you want to pass specific context
    return render(request, 'subscription_page.html')

def finalize_recycler_signup(request):
    # This view now assumes the user has successfully subscribed
    # Now, directly handle user creation and profile setup here
    if request.method == 'POST':
        form = RecyclerSignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            RecyclerProfile.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                location=form.cleaned_data['location']
            )
            group, created = Group.objects.get_or_create(name='Recyclers')
            user.groups.add(group)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('recycler_dashboard')
    else:
        form = RecyclerSignUpForm()
    return render(request, 'recycler_signup.html', {'form': form})


@csrf_exempt
def paypal_ipn_listener(request):
    # No changes needed here
    # This function handles PayPal IPN data
    pass

def handle_verified_ipn(ipn_data):
    # Handle IPN data from PayPal. This function should update user subscriptions
    # based on 'ipn_data' dict. Example:
    # Check `ipn_data` for subscription details and user identity,
    # then update user's subscription status in your database.
    pass


@login_required
def recycler_dashboard(request):
    try:
        profile = request.user.recycler_profile
    except RecyclerProfile.DoesNotExist:
        # Handle cases where the user does not have a recycler profile
        context = {'error': 'You do not have a recycler profile.'}
        return render(request, 'error_template.html', context)

    # Fetch only the latest 5 appointments
    appointments = profile.appointments.all().order_by('-appointment_date')[:5]
    context = {
        'profile': profile,
        'appointments': appointments,
        # Use .count() on the full queryset without slicing for the total count
        'appointments_count': profile.appointments.count()
    }
    return render(request, 'recycler_dashboard.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import RecyclerProfile

import logging
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import RecyclerProfile
from django.contrib.auth.models import Group
from django.contrib import messages

logger = logging.getLogger(__name__)

# Import necessary modules at the top
import logging
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from .models import RecyclerProfile, Subscription
from django.shortcuts import render, redirect
from django.contrib import messages

# Initialize logger
logger = logging.getLogger(__name__)

def subscription_success(request):
    logger.debug("Entered subscription_success view.")
    form_data = request.session.get('recycler_signup_form_data')
    
    if not form_data:
        logger.debug("No session data found. Redirecting to signup.")
        messages.error(request, "Signup session expired or not found. Please sign up again.")
        return redirect('recycler_signup')
    
    try:
        # Split user creation and profile creation
        user_data = {
            'username': form_data['username'],
            'email': form_data['email'],
            'password': form_data['password1']  # Change 'password1' to 'password' as expected by create_user
        }
        profile_data = {
            'company_name': form_data['company_name'],
            'location': form_data['location']
        }
        
        # Check if user exists
        if User.objects.filter(username=user_data['username']).exists():
            user = authenticate(username=user_data['username'], password=user_data['password'])
            if not user:
                logger.error("User exists but password mismatch.")
                messages.error(request, "An account with this username already exists with a different password.")
                return redirect('login')
        else:
            # User doesn't exist, so create new user and recycler profile
            user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=user_data['password'])
            RecyclerProfile.objects.create(user=user, **profile_data)
            group, _ = Group.objects.get_or_create(name='Recyclers')
            user.groups.add(group)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Logging in the user

        # Clear the session data after successful signup
        if 'recycler_signup_form_data' in request.session:
            del request.session['recycler_signup_form_data']

        logger.debug("Successfully handled subscription. Redirecting to dashboard.")
        return redirect('recycler_dashboard')
    except Exception as e:
        logger.error(f"Error processing subscription_success: {str(e)}")
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect('recycler_signup')



    
def subscription_cancel(request):
    # Handle subscription cancellation
    return render(request, 'subscription_cancel.html')


@login_required
def generator_dashboard(request):
    # Your existing logic to fetch profile and appointments...
    profile = request.user.generator_profile

    # Fetch messages linked to the generator's appointments, authored by recyclers
    messages = AppointmentMessage.objects.filter(
        appointment__generator_name=profile,
        author__recycler_profile__isnull=False  # Ensures the message author is a recycler
    ).select_related('author').order_by('-created_at')[:5]  # Adjust as needed

    # Count messages from each recycler
    message_counts = AppointmentMessage.objects.filter(
        appointment__generator_name=profile,
        author__recycler_profile__isnull=False
    ).values('author__username').annotate(total=Count('id')).order_by('-total')

    context = {
        'profile': profile,
        'messages': messages,
        'message_counts': message_counts,  # Add the message counts to the context
    }
    return render(request, 'generator_dashboard.html', context)

@login_required
def detailed_messages(request):
    profile = request.user.generator_profile

    messages = AppointmentMessage.objects.filter(
        appointment__generator_name=profile
    ).select_related('author', 'appointment').order_by('-created_at')

    return render(request, 'detailed_messages.html', {'messages': messages})

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(AppointmentMessage, id=message_id)

    # Check if the user is allowed to delete the message
    if request.user != message.appointment.generator_name.user and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this message.")

    message.delete()
    messages.success(request, "Message deleted successfully.")
    return HttpResponseRedirect(reverse('generator_dashboard'))  # Redirect back to the dashboard

def generator_signup(request):
    if request.method == 'POST':
        form = GeneratorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the user object without committing to DB
            user.save()

            # Check if the GeneratorProfile already exists
            profile, created = GeneratorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'company_name': form.cleaned_data.get('company_name'),
                    'location': form.cleaned_data.get('location'),
                }
            )
            
            # If the profile was not created, it means it already exists, and you may want to update it
            if not created:
                profile.company_name = form.cleaned_data.get('company_name')
                profile.location = form.cleaned_data.get('location')
                profile.save()

            # Add to Generator group
            group, _ = Group.objects.get_or_create(name='Generators')  # Ensure the group exists
            user.groups.add(group)

            return redirect('login')
    else:
        form = GeneratorSignUpForm()
    return render(request, 'generator_signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            # Check user group and redirect accordingly
            if user.groups.filter(name='Generators').exists():
                # Redirect to the recycler list if user is a Generator
                return redirect(reverse('recycler_list'))  # Ensure you have a URL named 'recycler_list'
            elif user.groups.filter(name='Recyclers').exists():
                # Redirect to the generator list if user is a Recycler
                return redirect(reverse('generator_list'))  # Ensure you have a URL named 'generator_list'
            else:
                # Redirect to a default page if user doesn't belong to any specific group
                return redirect(reverse('upload_image'))  # Adjust this to your default redirection URL
        else:
            # No backend authenticated the credentials
            return render(request, 'login.html', {
                'error_message': 'Invalid login credentials.'
            })
    else:
        # No post data available, let's just show the login page.
        return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    # Redirect to homepage or login page after logout
    return redirect('login')  # Replace 'login' with the name of the URL you want to redirect to


def appointment_success(request):
    return render(request, 'appointment_success.html')

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Appointment
from .forms import AppointmentForm
from .utils import send_appointment_email

import logging
logger = logging.getLogger(__name__)


class book_appointment(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'book_appointment.html'
    success_url = reverse_lazy('success_url')

    def form_valid(self, form):
        # Check if the user belongs to the 'Generators' group
        user_groups = self.request.user.groups.values_list('name', flat=True)
        if 'Generators' in user_groups:
            try:
                # Assuming 'generatorprofile' is the related_name set in the GeneratorProfile model
                generator_profile = self.request.user.generator_profile
                form.instance.generator_name = generator_profile
            except GeneratorProfile.DoesNotExist:
                # If the GeneratorProfile does not exist, handle appropriately
                # For example, redirect to a profile creation page
                return redirect('generator_signup')  # Adjust URL name as necessary
        else:
            # If the user is not in the 'Generators' group, handle appropriately
            # Example: render an error message or redirect
            return render(self.request, 'error_template.html', {
                'message': 'You must be in the Generators group to create an appointment.'
            })

        response = super().form_valid(form)
        send_appointment_email(self.object)
        return response
    
from django.shortcuts import get_object_or_404, render
from .models import Appointment

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    # Check if the user is allowed to view the conversation
    if not request.user.is_staff and request.user != appointment.generator_name.user and request.user != appointment.recycler_name.user:
        raise PermissionDenied("You are not allowed to view this page.")

    messages_list = AppointmentMessage.objects.filter(appointment=appointment)

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            AppointmentMessage.objects.create(appointment=appointment, author=request.user, message=message_text)
            # Optionally, add a success message or send notifications here
            messages.success(request, 'Your message has been sent.')
            return HttpResponseRedirect(request.path_info)  # Redirect to the same page

    return render(request, 'appointment_detail.html', {'appointment': appointment, 'messages': messages_list})

def recycling_education(request):
    # You can pass additional context to the template if needed
    return render(request, 'recycling_education.html')

# In your views.py

import logging
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Payment
# Ensure you've imported the necessary PayPal SDK classes
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

logger = logging.getLogger(__name__)

def get_paypal_client():
    # Returns PayPal HTTP client with the correct environment
    if settings.PAYPAL_ENVIRONMENT == 'sandbox':
        environment = SandboxEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)
    else:
        # Assume live environment if not sandbox
        environment = LiveEnvironment(client_id=settings.PAYPAL_CLIENT_ID, client_secret=settings.PAYPAL_CLIENT_SECRET)
    return PayPalHttpClient(environment)

@login_required
def create_paypal_order(request):
    logger.info("Creating PayPal order...")
    # Initialize the PayPal client
    client = get_paypal_client()
    
    # Initialize your request to PayPal
    paypal_request = OrdersCreateRequest()  # Be careful not to shadow the 'request' from Django
    paypal_request.prefer('return=representation')
    paypal_request.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": "USD", "value": "10.00"}}]
    })

    try:
        # Execute the request
        response = client.execute(paypal_request)
        logger.info(f"PayPal order created successfully: {response.result.id}")

        # Record the successful order in your Django app
        Payment.objects.create(
            payer=request.user,
            amount="10.00",
            paypal_order_id=response.result.id
        )

        return JsonResponse({'id': response.result.id})
    except Exception as e:
        logger.error(f"Error creating PayPal order: {e}")
        return JsonResponse({'error': str(e)}, status=500)



def payment_page(request):
    # Render the template that contains your PayPal button and JavaScript SDK integration
    return render(request, 'payment.html', {})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Count
from .models import Payment, Appointment
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
from datetime import datetime  # Import datetime

@login_required
def recycler_stats(request):
    recycler_profile = request.user.recycler_profile

    payments = (
        Payment.objects.filter(payer=request.user)
        .annotate(month=ExtractMonth('created_at'), year=ExtractYear('created_at'))
        .values('month', 'year')
        .annotate(count=Count('id'))
        .order_by('year', 'month')
    )

    appointments = (
        Appointment.objects.filter(recycler_name=recycler_profile)
        .annotate(month=ExtractMonth('appointment_date'), year=ExtractYear('appointment_date'))
        .values('month', 'year')
        .annotate(count=Count('id'))
        .order_by('year', 'month')
    )

    payments_data = defaultdict(int)
    appointments_data = defaultdict(int)

    for entry in payments:
        date_key = f"{entry['year']}-{entry['month']:02d}"
        payments_data[datetime.strptime(date_key, '%Y-%m')] += entry['count']

    for entry in appointments:
        date_key = f"{entry['year']}-{entry['month']:02d}"
        appointments_data[datetime.strptime(date_key, '%Y-%m')] += entry['count']

    dates = sorted(set(payments_data.keys()) | set(appointments_data.keys()))
    payments_counts = [payments_data[date] for date in dates]
    appointments_counts = [appointments_data[date] for date in dates]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, payments_counts, label='Payments', marker='o', linestyle='-')
    plt.plot(dates, appointments_counts, label='Appointments', marker='o', linestyle='-')

    plt.title('Your Monthly Payments and Appointments Stats')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.xticks(dates, rotation=45)
    plt.legend()

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    context = {'graph': f"data:image/png;base64,{data}"}

    plt.close()

    return render(request, 'recycler_stats.html', context)





