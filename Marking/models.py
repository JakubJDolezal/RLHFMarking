from django.db import models

class Question(models.Model):
    text = models.TextField(default='Default question')

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(default='Default response')
    score = models.IntegerField(default=5)