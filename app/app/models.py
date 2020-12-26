from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=12)
    pswd = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.userId