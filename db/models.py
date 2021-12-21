from django.db import models


# Create your models here.

class Keyword(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)

    # display name in admin
    def __str__(self):
        return self.name

    def method(self):
        pass

    @classmethod
    def class_method(cls):
        pass


class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name

    # meta data for django admin
    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "A Category"


class Post(models.Model):
    name = models.CharField(max_length=200, blank=False)
    # file will be uploaded to MEDIA_ROOT/uploads/posts/
    image = models.ImageField(upload_to='uploads/posts/', blank=True, null=True)
    # on_delete=models.CASCADE => when category was deleted, all corresponding posts are also deleted
    # related_name => `category.posts` contains all posts related to category
    category = models.ForeignKey("db.Category", blank=False, on_delete=models.CASCADE, related_name="posts")
    # cross table will be auto created by django
    # related_name => `keyword.posts` contains all posts related to keyword
    keywords = models.ManyToManyField("db.Keyword", related_name="posts")

    def __str__(self):
        return f"{self.category}: {self.name}"
