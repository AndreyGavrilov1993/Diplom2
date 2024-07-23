from django.db import models

class Feedback(models.Model):
    message = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
