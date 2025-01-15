# from email.mime.text import MIMEText
# import logging
# import smtplib
# import time
# from fastapi import HTTPException
# from PIL import Image as PILImage
# from typing import List
# from models import ConvertPDFModel, ConvertPDFOutputModel

# # Set up logging configuration (you can place this in your main.py or settings)
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def send_failure_notification(error_message: str, email_id: str):
#     try:
#         # Setup your email server and sender/receiver details
#         from_email = "your-email@example.com"
#         to_email = "admin@example.com"  # Or set as user's email if applicable
#         subject = "PDF Conversion Failure Notification"
#         body = f"PDF Conversion failed for user {email_id}.\nError: {error_message}"

#         msg = MIMEText(body)
#         msg['Subject'] = subject
#         msg['From'] = from_email
#         msg['To'] = to_email

#         # Connect to SMTP server and send email
#         with smtplib.SMTP('smtp.example.com', 587) as server:
#             server.starttls()
#             server.login("your-email@example.com", "your-email-password")
#             server.sendmail(from_email, to_email, msg.as_string())
        
#         logging.info(f"Sent failure notification to {to_email}")

#     except Exception as e:
#         logging.error(f"Failed to send failure notification: {e}")

# def send_success_notification(email_id: str, filename: str):
#     """
#     Sends a success notification (e.g., email) about successful PDF conversion.

#     Args:
#     - email_id: User's email ID
#     - filename: Name of the converted PDF file
#     """
#     try:
#         # Setup your email server and sender/receiver details
#         from_email = "your-email@example.com"
#         to_email = email_id
#         subject = "PDF Conversion Success Notification"
#         body = f"Your PDF file {filename} has been successfully converted."

#         msg = MIMEText(body)
#         msg['Subject'] = subject
#         msg['From'] = from_email
#         msg['To'] = to_email

#         # Connect to SMTP server and send email
#         with smtplib.SMTP('smtp.example.com', 587) as server:
#             server.starttls()
#             server.login("your-email@example.com", "your-email-password")
#             server.sendmail(from_email, to_email, msg.as_string())
        
#         logging.info(f"Sent success notification to {to_email}")

#     except Exception as e:
#         logging.error(f"Failed to send success notification: {e}")


# def log_conversion_success(filename: str, email_id: str, time_taken: float):
#     """
#     Logs the success of PDF conversion.

#     Args:
#     - filename: Name of the converted PDF file
#     - email_id: User's email ID
#     - time_taken: Time taken for the conversion process (in seconds)
#     """
#     logger.info(f"PDF conversion successful for {filename} (Email: {email_id}) - Time Taken: {time_taken:.2f} seconds")

# fail.py (Inside the Fail folder)
from email.mime.text import MIMEText
import logging
import smtplib

# Set up logging configuration (you can place this in your main.py or settings)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_failure_notification(error_message: str, email_id: str):
    try:
        # Setup your email server and sender/receiver details
        from_email = "your-email@example.com"
        to_email = "admin@example.com"  # Or set as user's email if applicable
        subject = "PDF Conversion Failure Notification"
        body = f"PDF Conversion failed for user {email_id}.\nError: {error_message}"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Connect to SMTP server and send email
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login("your-email@example.com", "your-email-password")
            server.sendmail(from_email, to_email, msg.as_string())
        
        logging.info(f"Sent failure notification to {to_email}")

    except Exception as e:
        logging.error(f"Failed to send failure notification: {e}")

def send_success_notification(email_id: str, filename: str):
    """
    Sends a success notification (e.g., email) about successful PDF conversion.

    Args:
    - email_id: User's email ID
    - filename: Name of the converted PDF file
    """
    try:
        # Setup your email server and sender/receiver details
        from_email = "your-email@example.com"
        to_email = email_id
        subject = "PDF Conversion Success Notification"
        body = f"Your PDF file {filename} has been successfully converted."

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Connect to SMTP server and send email
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login("your-email@example.com", "your-email-password")
            server.sendmail(from_email, to_email, msg.as_string())
        
        logging.info(f"Sent success notification to {to_email}")

    except Exception as e:
        logging.error(f"Failed to send success notification: {e}")

def log_conversion_success(filename: str, email_id: str, time_taken: float):
    """
    Logs the success of PDF conversion.

    Args:
    - filename: Name of the converted PDF file
    - email_id: User's email ID
    - time_taken: Time taken for the conversion process (in seconds)
    """
    logger.info(f"PDF conversion successful for {filename} (Email: {email_id}) - Time Taken: {time_taken:.2f} seconds")
