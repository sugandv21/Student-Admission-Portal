from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

SIGNATURE = "\n\nRegards,\nAdmissions Office,\nVTS Academy"

def send_app_received_email(appn):
    """
    Sends a confirmation email to the applicant after they submit the form.
    """
    subject = "Application Received"
    body = (
        f"Hello {appn.full_name},\n\n"
        "We have received your application. Our admissions team will review it soon.\n\n"
        "Status: PENDING"
        f"{SIGNATURE}"
    )
    _send_email(to=[appn.email], subject=subject, body=body)

def send_status_update_email(appn):
    """
    Sends an email to the applicant when admin approves/rejects the application.
    """
    subject = f"Application {appn.status}"
    body = (
        f"Hello {appn.full_name},\n\n"
        f"Your application status has been updated to: {appn.status}."
        f"{SIGNATURE}"
    )
    _send_email(to=[appn.email], subject=subject, body=body)

def send_admin_new_application_email(appn):
    """
    Sends a notification email to admin(s) whenever a new application is submitted.
    Recipients:
      - ADMIN_NOTIFY_EMAIL (or ADMIN_EMAIL fallback)
      - MAIL_USERNAME (EMAIL_HOST_USER)
    """
    admin_to = current_app.config.get("ADMIN_NOTIFY_EMAIL") or current_app.config.get("ADMIN_EMAIL")
    mail_username = current_app.config.get("MAIL_USERNAME")  # EMAIL_HOST_USER

    # Build unique recipient list (skip Nones/empties, dedupe case-insensitively)
    recipients = []
    for addr in (admin_to, mail_username):
        if addr:
            addr = addr.strip()
            if addr and addr.lower() not in [a.lower() for a in recipients]:
                recipients.append(addr)

    if not recipients:
        return  # no admin recipients configured; safely skip

    subject = "New Student Application Submitted"
    body = (
        "A new student application has been submitted.\n\n"
        f"ID: {appn.id}\n"
        f"Name: {appn.full_name}\n"
        f"Email: {appn.email}\n"
        f"Phone: {appn.phone}\n"
        f"Course: {appn.course}\n"
        f"Submitted (UTC): {appn.created_at}"
        f"{SIGNATURE}"
    )
    _send_email(to=recipients, subject=subject, body=body)

def _send_email(to, subject, body):
    """
    Internal helper to send a plain-text email using Flask-Mail.
    """
    msg = Message(subject=subject, recipients=to, body=body)
    mail.send(msg)
