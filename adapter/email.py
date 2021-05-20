from django.core.mail import EmailMultiAlternatives


class EmailAdapter:
    def __init__(self, email):
        self.email = email

    def send_email(self, has_attachments=False, file_path=None):
        mail_subject = 'Weather Data Excel'
        to_email = self.email
        email = EmailMultiAlternatives(mail_subject, to=[to_email])
        if has_attachments:
            if file_path:
                email.attach_file(file_path)
        email.send()
