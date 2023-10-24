from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=45, null=False)
    born_date = models.CharField(max_length=45, null=False)
    description = models.CharField(null=False)
    born_location = models.CharField(max_length=80, null=False)
    goodreads_url = models.CharField(max_length=80, null=True   )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.fullname}"