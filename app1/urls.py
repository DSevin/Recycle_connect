from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('classification-result/', views.classification_result, name ='classification_result'),
    path('recyclers/', views.recycler_list, name='recycler_list'),
    path('generators/', views.generator_list, name='generator_list'),
    path('signup/recycler/', views.recycler_signup, name ='recycler_signup'),
    path('finalize-signup/', views.finalize_recycler_signup, name='finalize_recycler_signup'),
    path('signup/generator/', views.generator_signup, name ='generator_signup'),
    path('login/', views.login_view, name ='login'),
    path('logout/', views.logout_view, name ='logout'),
    path('recycler/dashboard/', views.recycler_dashboard, name ='recycler_dashboard'),
    path('generator/dashboard/', views.generator_dashboard, name ='generator_dashboard'),
    path('book-appointment/', views.book_appointment.as_view(), name ='book_appointment'),
    path('appointment-success/', views.appointment_success, name='success_url'),  # New URL pattern
    #path('paypal-ipn/', views.paypal_ipn_listener, name='paypal_ipn_listener'),
    path('subscription/success/', views.subscription_success, name='subscription_success'),
    path('subscription/cancel/', views.subscription_cancel, name='subscription_cancel'),
    path('signup/subscription/', views.subscription_page, name='subscription_page'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    #path('full-appointment/', views.full_appointments, name ='full_appointments'),
    path('messages/detailed/', views.detailed_messages, name='detailed_messages'),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('generator-list/', views.generator_list, name ='generator_list'),
    path('recycler-list/', views.recycler_list, name ='recycler_list'),
    path('recycling-education/', views.recycling_education, name='recycling_education'),
    path('payment/', views.payment_page, name='payment_page'),
    path('create-paypal-order/', views.create_paypal_order, name='create_paypal_order'),
    # Add other URLs as needed
]