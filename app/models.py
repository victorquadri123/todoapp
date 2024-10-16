from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    TaskTitle = models.CharField(max_length=50,default="tasktitle", null=False)
    Description = models.TextField(null=True, blank=True)
    DueDate = models.DateTimeField(db_column= "duedate")
    CompletedDate = models.DateTimeField(null=True, blank=True)
    CreatedDate = models.DateTimeField(default= timezone.now)
    Important = models.BooleanField(default=False)
    Status = models.CharField(max_length= 50, default="pending")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

