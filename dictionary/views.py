from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView, ListView

from .models import Article, User
from .forms import ArticleForm
from django.http import HttpResponse
from django.views.generic.base import View
from django.db.models import Q


# def index(request):
#     articles = Article.objects.all()
#     return render(request, "dictionary/index.html", {'title': 'Главная страница сайта', 'articles': articles})

# def search(request):
#     articles = Article.objects.filter(keywords__name='要')
#     return render(request, "dictionary/search.html", {'title': 'Результаты поиска', 'articles': articles})


def about(request):
    articles = Article.objects.all()
    return render(request, "dictionary/search.html", {'title': 'Главная страница сайта', 'articles': articles})


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


class ArticleDetailView(DetailView):
    """Полный текст и описание стат"""
    model = Article
    slug_field = "url"
    # def get(self, request, slug):
    #     article = Article.objects.get(url=slug)
    #     return render(request, "dictionary/article_detail.html", {
    #         "article": article
    #     })


class AuthorDetailView(DetailView):
    """Полный текст и описание статьи"""
    model = User
    slug_field = "username"
    template_name = "dictionary/author.html"
#     def get(self, request, slug):
#         author = User.objects.get(url=slug)
#         return render(request, "dictionary/author_detail.html", {
#             "author": author
#         })


class HomePageView(TemplateView):
    template_name = 'dictionary/index.html'


class SearchResultsView(ListView):
    model = Article
    template_name = 'dictionary/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Article.objects.filter(
            Q(keywords__name=query)
        )
        return object_list