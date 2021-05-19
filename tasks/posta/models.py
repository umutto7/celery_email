from django.db import models

# Create your models here.

class Dava(models.Model):
    index = models.IntegerField()
    manager_mail = models.CharField(max_length=30)
    text = models.TextField()
    deadline1 = models.DateField()
    deadline2 = models.DateField()
    deadline3 = models.DateField()
