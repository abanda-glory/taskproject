from django.db import models
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='task')
    # user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='task')
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

