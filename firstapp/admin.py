from django.contrib import admin

from firstapp import models

# Register your models here.

admin.site.register(models.enquiry)
admin.site.register(models.registeredUsers)
admin.site.register(models.reviews)
admin.site.register(models.blogs)
admin.site.register(models.news)
admin.site.register(models.athletes)
# admin.site.register(models.league)

admin.site.register(models.match)



admin.site.register(models.videosnew)

