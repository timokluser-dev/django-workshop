from django.contrib import admin

# Register your models here.
from db.models import Keyword, Category, Post

admin.site.register(Keyword)
admin.site.register(Category)
admin.site.register(Post)
