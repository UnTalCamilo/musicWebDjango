from django.contrib import admin
from .models import Song, LikedSong, History

# Register your models here.
admin.site.register(Song)
admin.site.register(LikedSong)
admin.site.register(History)