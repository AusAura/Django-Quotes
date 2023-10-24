from django.db import models
from django.contrib.auth.models import User
from authorsapp.models import Author

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]
    

class Quote(models.Model):
    quote = models.CharField(max_length=1500, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.quote}"
    
