from io import BytesIO
from tensorflow.keras.preprocessing import image
import numpy as np

from django.core.mail import send_mail
from django.conf import settings

def preprocess_image(image_file, target_size):
    image_file.seek(0)  # Reset file pointer to the start
    img_bytes = BytesIO(image_file.read())  # Create a BytesIO object from the uploaded file

    img = image.load_img(img_bytes, target_size=target_size)  # Load the image for processing
    img_array = image.img_to_array(img)  # Convert the image to an array
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)  # Expand dimensions to fit model input
    return img_array_expanded_dims / 255.0  # Normalize pixel values as done during training


def process_prediction(prediction):
    # Assuming your model outputs probabilities for each class
    classes = ['HDPE', 'LDPE', 'Other Plastic', 'PET']  # Adjust based on your actual classes
    class_index = np.argmax(prediction)
    return classes[class_index]

def send_appointment_email(appointment):
    subject = 'Appointment Booking Confirmation'
    message = f"Dear {appointment.recycler_name.user.username},\n\n" \
              f"You have a new appointment with {appointment.generator_name.user.username} on {appointment.appointment_date.strftime('%Y-%m-%d %H:%M')}.\n" \
              f"Details: {appointment.details}\n\n" \
              f"Best regards,\nRecycle Connect Team"
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [appointment.recycler_name.user.email],
        fail_silently=False,
    )