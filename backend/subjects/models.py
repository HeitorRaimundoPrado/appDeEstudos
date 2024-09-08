from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from communities.models import Community
from bookmarks.models import Bookmarkable
from django.core.validators import FileExtensionValidator

# Create your models here.
class Subject(models.Model):
    description = models.TextField()
    name = models.CharField(max_length=50)

class ForumPost(Bookmarkable):
    title = models.CharField(max_length=100, blank=True)
    private = models.BooleanField(default=False)
    is_social = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, related_name="posts", on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    community = models.ForeignKey(Community, blank=True, null=True, related_name="posts", on_delete=models.CASCADE)
    parent_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="answers")
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    positive = models.BooleanField()
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="votes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_post_user')
        ]


def get_filename(instance, filename):
    file_split = filename.split('.')
    base_name, ext = ''.join(file_split[:-1]), file_split[-1]
    return 'uploads/' + base_name + '-' + str(instance.post.id) + '.' + ext

class PostAttachment(models.Model):
    post = models.ForeignKey(ForumPost, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_filename, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)

