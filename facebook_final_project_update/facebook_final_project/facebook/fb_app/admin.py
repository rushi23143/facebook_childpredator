from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Certificate)
admin.site.register(Coment)
admin.site.register(Prediator)
admin.site.register(Profile)
admin.site.register(ImagePre)
admin.site.register(FriendList)
admin.site.register(UserStatus)
admin.site.register(FriendRequest)
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id','photo','date','name']