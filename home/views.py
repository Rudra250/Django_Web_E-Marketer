from django.shortcuts import render,redirect
from datetime import datetime
from home.models import Contact,Database,Verification,Verification3
from django.contrib import messages
from random import *
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.urls import reverse
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders

# Create your views here.
def index(request):
    return render(request, 'index.html')
    messages.success(request,"This is test message")

def about(request):
    return render(request, 'About.html')

def contact(request): 
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, "Your form is submitted, Thank you.")
    return render(request, 'contact.html')

def database(request):
    if request.method == 'POST':
        emailaddress = request.POST.get('emailaddress')
        database = Database(emailaddress=emailaddress,date=datetime.today())
        database.save()
        messages.success(request, "Email address is successfully submitted, Thank You.")
    return render(request, 'database.html')

def verification(request):

    global verifyemail

    if request.method == 'POST':
        verifyemail = request.POST.get('verifyemail')
        otp = str(random.randint(1000,9999))
        verification = Verification(verifyemail=verifyemail,otp=otp,date=datetime.today())
        verification.save()
        send_OTP(verifyemail,otp)
        return redirect('/verification2')
    return render(request, 'verification.html')

def send_OTP(verifyemail,otp):

    sender_email = 'YOUR TEMPORARY EMAIL ADDRESS'
    receiver_email = verifyemail
    subject = 'OTP Verification'
    body = f'Hey this the message from E-Marketer, Your OTP is: {otp}'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = 'YOUR ACCOUNTS APP PASSWORD'

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

def verification2(request):
    if request.method == 'POST':
        OTP = request.POST.get('OTP')
        latest_verification = Verification.objects.latest('id')
        latest_otp = latest_verification.otp
        
        if OTP == latest_otp:
            verifyemail = latest_verification.verifyemail
            return redirect('verification3')
        else:
            messages.error(request, "Invalid OTP")
            return render(request, 'verification2.html')
    return render(request, 'verification2.html')

def verification3(request):
    if request.method == 'POST':
        SenderEmail = request.POST.get('SenderEmail')
        if SenderEmail == verifyemail:
            SenderPassword = request.POST.get('SenderPassword')
            SenderSubject = request.POST.get('SenderSubject')
            EmailDesc = request.POST.get('EmailDesc')
            uploaded_file = request.FILES['file']
            
            verification3 = Verification3(SenderEmail=SenderEmail, SenderSubject=SenderSubject, EmailDesc=EmailDesc,date=datetime.today())
            verification3.save()

            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(uploaded_file.read())
            encoders.encode_base64(attachment)

            attachment.add_header(
                "Content-Disposition",
                f"attachment; filename={uploaded_file.name}",
            )

            try:
                email_addresses = Database.objects.all()

                for email_object in email_addresses:
                    receiver_email = email_object.emailaddress

                    message = MIMEMultipart()
                    message["From"] = SenderEmail
                    message["To"] = receiver_email
                    message["Subject"] = SenderSubject

                    message.attach(MIMEText(EmailDesc, "plain"))

                    message.attach(attachment)
                    text = message.as_string()

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(SenderEmail, SenderPassword)
                        server.sendmail(SenderEmail, receiver_email, text)

                return redirect("final")
            except smtplib.SMTPAuthenticationError:
                messages.error(request, "Invalid Email address or Password")
            except:
                messages.error(request, "An error occurred during sending emails.")
        else:
            messages.error(request, "Please enter a verified email address")
            return render(request, 'verification3.html')

    return render(request, 'verification3.html')

def final(request):
    return render(request,"final.html")

def privacypolicy(request):
    return render(request,"privacy&policy.html")
