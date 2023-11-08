from email import contentmanager
from email.mime import image
from django.db import models
from datetime import date

# Create your models here.

class enquiry(models.Model):
    username=models.CharField(max_length=30)
    emailid=models.EmailField()
    message=models.TextField()
  
class registeredUsers(models.Model):
    username=models.CharField(max_length=30)
    emailid=models.EmailField()
    password=models.CharField(max_length=30)
    registerDate=models.DateField(default=date.today())
    phoneNumber=models.CharField(max_length=10,null=True)
    profilePicture=models.ImageField(null=True ,blank=True)
    dob=models.CharField(null=True,blank=True,max_length=100)
    gender=models.CharField(max_length=1,choices=[('m','male'),('f','female')],default='m')
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):

        return self.username

class reviews(models.Model):
    subject=models.CharField(max_length=500)
    message=models.TextField()
    user=models.ForeignKey(registeredUsers,on_delete=models.CASCADE)
    reviewDate=models.DateField(default=date.today())

class blogs(models.Model):
    title=models.CharField(max_length=200,null=True)
    image=models.ImageField()
    content=models.TextField()
    addedon=models.DateField(default=date.today())

class news(models.Model) :
    headline=models.CharField(max_length=100)
    image=models.ImageField()
    content=models.TextField()
    date=models.DateField(default=date.today())

class athletes(models.Model):
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    image=models.ImageField()
    bannerImage=models.ImageField(null=True)

    win=models.IntegerField()
    lose=models.IntegerField()
    draw=models.IntegerField()
    age=models.IntegerField(null=True)
    nickname=models.CharField(max_length=30)
    weight=models.CharField(max_length=100)
    division=models.CharField(max_length=100)
    facebook=models.CharField(max_length=100,null=True,blank=True)
    twitter=models.CharField(max_length=100,null=True,blank=True)
    instagram=models.CharField(max_length=100,null=True,blank=True)
    height=models.CharField(max_length=6,null=True)
    winstreak=models.IntegerField(null=True)
    sub=models.IntegerField(null=True)
    ko=models.IntegerField(null=True)

    def __str__(self):
        return self.name


# class league(models.Model):
#     stadium=models.CharField(max_length=100)
#     location=models.CharField(max_length=100)

class match(models.Model):
    athlete1=models.ForeignKey(athletes,on_delete=models.CASCADE, related_name='athlete1')
    athlete2=models.ForeignKey(athletes,on_delete=models.CASCADE,related_name='athlete2',null=True)
    matchDate=models.DateField(default=date.today())
    matchTime=models.TimeField()
    location=models.CharField(max_length=100,null=True)
    result=models.CharField(max_length=100,null=True,blank=True)

    
    def __str__(self):
        return self.athlete1.division
    





class videosnew(models.Model):
    title=models.TextField()   
    video=models.TextField()  
    def __str__(self):
        return self.title      










    
