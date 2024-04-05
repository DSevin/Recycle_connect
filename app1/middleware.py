from django.urls import resolve, reverse
from django.shortcuts import redirect
from .models import Subscription


class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            # Excluding dashboard view from subscription checks
            exempt_urls = ['recycler_dashboard', 'subscription_page', 'subscription_success', 'subscription_cancel', 'login', 'logout', 'recycler_signup']

            current_url_name = resolve(request.path_info).url_name
            if current_url_name in exempt_urls:
                return None  # Skip middleware for these URLs

            try:
                subscription = Subscription.objects.get(user=request.user)
                if not subscription.is_active:
                    return redirect('subscription_page')
            except Subscription.DoesNotExist:
                return redirect('subscription_page')

