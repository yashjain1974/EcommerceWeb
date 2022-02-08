from django.db import models
from django.utils import timezone
# Create your models here.
class Blogpost(models.Model):
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100,default="")
    author=models.CharField(max_length=100,default="")
    head0=models.CharField(max_length=100,default="")
    content_head0=models.TextField(max_length=5000,default="")
    head1 = models.CharField(max_length=100, default="")
    content_head1=models.TextField(max_length=5000,default="")
    head2 = models.CharField(max_length=100, default="")
    content_head2=models.TextField(max_length=5000,default="")
    pub_date=models.DateField(default=timezone.now())
    thumbnail = models.ImageField(upload_to='blog/images', default="")

    def __str__(self):
        return self.title


