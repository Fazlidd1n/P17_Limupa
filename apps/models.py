import uuid
import time

from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, CASCADE, DateTimeField, ImageField, ForeignKey, ManyToManyField, \
    UUIDField, EmailField
from django_resized import ResizedImageField

from apps.tasks import task_send_email


class User(AbstractUser):
    image = ResizedImageField(size=[90, 90], crop=['middle', 'center'], upload_to='users/images',
                              default='users/defoult_user.jpeg')


class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = ResizedImageField(size=[570, 365], crop=['middle', 'center'], upload_to='blog/images/',
                              default='blog/images/defoult.jpeg')
    name = CharField(max_length=255)
    author = ForeignKey('apps.User', CASCADE, 'blogs')
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    tags = ManyToManyField('apps.Tag')
    text = RichTextField(blank=True, null=True)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        emails: list = Newsletter_emails.objects.values_list('email', flat=True)
        task_send_email.delay("Yangi blog qoshildi", self.name, list(emails))

    def __str__(self):
        return self.name

    def count_comment(self):
        return self.comment_set.count()


class Comment(Model):
    text = CharField(max_length=255)
    blog = ForeignKey('apps.Blog', CASCADE)
    author = ForeignKey('apps.User', CASCADE, 'comments')
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)


class Newsletter_emails(Model):
    email = EmailField()
