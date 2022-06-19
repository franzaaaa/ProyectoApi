from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_email(data):
        print('Enviado')
        email = EmailMessage(subject=data['subject'], body=data['body'], to=(data['email'],))
        email.send()