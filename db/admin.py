from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

# Register your models here.
from db.models import Keyword, Category, Post

admin.site.register(Keyword)
admin.site.register(Category)
admin.site.register(Post)


# Wagtail
class PostAdmin(ModelAdmin):
    model = Post
    menu_label = 'Posts'
    menu_icon = 'doc-empty-inverse'  # icons: https://thegrouchy.dev/general/2015/12/06/wagtail-streamfield-icons.html
    menu_order = 101
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'category', 'written_by', 'date_published', 'date_modified')  # list view properties
    search_fields = ('name',)


modeladmin_register(PostAdmin)


class KeywordAdmin(ModelAdmin):
    model = Keyword
    menu_label = 'Keywords'
    menu_icon = 'openquote'
    menu_order = 102
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    search_fields = ('name',)


modeladmin_register(KeywordAdmin)


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = 'Categories'
    menu_icon = 'tag'
    menu_order = 103
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    search_fields = ('name',)


modeladmin_register(CategoryAdmin)
