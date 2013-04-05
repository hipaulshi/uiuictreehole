from django.db import models

# Create your models here.
class ContentModel(models.Model):
    ip = models.CharField(max_length=20, db_index=True)
    time = models.DateTimeField(db_index=True)
    contentstr=models.CharField(max_length=121, db_index=True)
