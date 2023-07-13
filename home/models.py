from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email= models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField(default=None)

    def __str__(self):
        return self.name
    
class Database(models.Model):
    emailaddress = models.CharField(max_length=122)
    date = models.DateField(default=None)

    def __str__(self):
        return self.emailaddress
    
class Verification(models.Model):
    verifyemail = models.CharField(max_length=122)
    otp = models.CharField(max_length=6, default='000000')
    date = models.DateField(default=None)

    def __str__(self):
        return self.verifyemail
    
class Verification3(models.Model):
    SenderEmail = models.CharField(max_length=122)
    SenderSubject = models.CharField(max_length=122,default='N/A')
    EmailDesc = models.CharField(max_length=122,default='N/A')
    date = models.DateField(default=None)
    
    def __str__(self):
        return self.SenderEmail