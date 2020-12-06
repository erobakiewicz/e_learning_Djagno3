from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User, related_name='course_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    student = models.ManyToManyField(User, related_name='courses_joined',
                                     blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # adding custom field OrderField for ordering modules in course
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order} - {self.title}"


"""
Model of generic content which can be associated with given Module.
For different types of content e.g. txt, image, video there will be one
generic model to connect them with Module model. via content_type and object_id
both connected by GenericForeignKey in "item".
"""


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'models__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file',
                                     )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    # adding custom field OrderField for ordering content with respect to module
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


# abstract model for all content types
class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# child models of an abstract model ItemBase
class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    image = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
