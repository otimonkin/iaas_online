from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm
from django.http import HttpResponse


def index(request):
    articles = Article.objects.all()
    return render(request, "dictionary/index.html", {'title': 'Главная страница сайта', 'articles': articles})


def about(request):
    return render(request, "dictionary/about.html")


def create(request):
    error = ''
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            error = 'Форма была заполнена некорректно'
            return HttpResponse(form.errors)

    form = ArticleForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, "dictionary/create.html", context)