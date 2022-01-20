from django import forms

from db.models import Post, Category, Keyword


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = '__all__'
