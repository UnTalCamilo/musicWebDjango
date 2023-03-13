from django.contrib import admin
from .models import Song, LikedSong, Playlist, PlaylistSong, History

# Register your models here.
admin.site.register(Song)
admin.site.register(LikedSong)
admin.site.register(Playlist)
admin.site.register(PlaylistSong)
admin.site.register(History)