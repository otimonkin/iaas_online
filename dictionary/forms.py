from .models import Article
from django.forms import ModelForm, TextInput, Textarea

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "message", "url"]  #"keywords",
        widgets ={
            'title': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Введите заголовок статьи"
            }),
            'message': Textarea(attrs={
                'class': "form-control",
                'placeholder': "Введите текст статьи"
            }),
            # 'keywords': TextInput(attrs={
            #     'class': "form-control",
            #     'placeholder': "Введите ключевые слова"
            # }),
            'url': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Придумайте URL"
            }),
        }