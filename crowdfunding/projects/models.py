from django.db import models
from django.contrib.auth import get_user_model

def image_upload_to(instance, filename):
    # You can modify this function to generate your desired filename
    return f"images/{filename}"

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    # image = models.URLField()
    image = models.ImageField(upload_to=image_upload_to, null=True, blank=True)
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_pledges'
    )