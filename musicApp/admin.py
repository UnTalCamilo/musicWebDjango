from django.contrib import admin
from .models import Singer, Song, SongSinger, Playlist

# Register your models here.
admin.site.register(Singer)
admin.site.register(Song)
admin.site.register(SongSinger)
admin.site.register(Playlist)
