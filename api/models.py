from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)
    email = models.EmailField(default='', max_length=254)
    
    def __str__(self):
        return self.title