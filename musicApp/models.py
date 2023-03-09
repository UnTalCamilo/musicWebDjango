from django.db import models
from django.contrib.auth.models import User

music_tags = (
    ('Pop', 'Pop'),
    ('Rock', 'Rock'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Jazz', 'Jazz'),
    ('Blues', 'Blues'),
    ('Folk', 'Folk'),
    ('Classical', 'Classical'),
    ('Electronic', 'Electronic'),
    ('Reggae', 'Reggae'),
    ('Metal', 'Metal'),
    ('Punk', 'Punk'),
    ('Disco', 'Disco'),
    ('Rap', 'Rap'),
    ('Alternative', 'Alternative'),
    ('Ska', 'Ska'),
    ('Reggaeton', 'Reggaeton'),
    ('Unknown', 'Unknown'),
)

# Create your models here.
class Singer(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/Singer')
    song = models.ManyToManyField('Song', related_name='singers')

    def __str__(self):
        return self.name
    

    
class Song(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/Song')
    file = models.FileField(upload_to='files/Song')
    tag = models.CharField(max_length=100, choices=music_tags, default='Unknown')
    year = models.IntegerField()

    def __str__(self):
        return self.name + ' - ' + self.tag
    
    
class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name