from django.shortcuts import render, redirect
from .models import Article, User
from .forms import ArticleForm
from django.http import HttpResponse
from django.views.generic.base import View


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



def authorview(request):
    """Список авторов"""
    authors = User.objects.all()
    return render(request, "dictionary/author_list.html", {
        "authors": authors
    })


class ArticleDetailView(View):
    """Полный текст и описание стат"""
    def get(self, request, slug):
        article = Article.objects.get(url=slug)
        return render(request, "dictionary/article_detail.html", {
            "article": article
        })

# class AuthorDetailView(View):
#     """Полный текст и описание статьи"""
#     def get(self, request, slug):
#         author = User.objects.get(url=slug)
#         return render(request, "dictionary/author_detail.html", {
#             "author": author
#         })