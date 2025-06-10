from django.db import models

class Task(models.Model):
    title = models.CharField('タイトル', max_length=200)
    isStared = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)
    due = models.DateTimeField(null=True, blank=True)
    completeDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title