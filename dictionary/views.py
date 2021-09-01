from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import DetailView, TemplateView, ListView

from .models import Article, User, Keyword
from .forms import ArticleForm
from django.http import HttpResponse
from django.views.generic.base import View, TemplateResponseMixin
from django.db.models import Q


# def index(request):
#     articles = Article.objects.all()
#     return render(request, "dictionary/index.html", {'title': 'Главная страница сайта', 'articles': articles})

# def search(request):
#     articles = Article.objects.filter(keywords__name='要')
#     return render(request, "dictionary/search.html", {'title': 'Результаты поиска', 'articles': articles})


# def all_articles(request):
#     articles = Article.objects.all()
#     return render(request, "dictionary/all_articles.html", {'title': 'Главная страница сайта', 'articles': articles})


def create(request):
    error = ''
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            #form = form.save(commit=False)
            #form.student = request.user
            #form.assignment_id = pk
            #form.save()

            article = form.save()
            article.authors.add(request.user)
            return redirect("index")
        else:
            error = 'Форма была заполнена некорректно'
            return HttpResponse(error)

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


class ArticleListView(ListView):
    model = Article


class ArticleDetailView(DetailView):
    """Полный текст и описание стат"""
    model = Article
    slug_field = "url"
    template_name = "dictionary/article.html"
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


class KeywordsView(ListView):
    model = Keyword


class KeywordDetailView(DetailView):
    model = Keyword
    slug_field = "name"
    template_name = "dictionary/keyword.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(KeywordDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['article_list'] = Article.objects.filter(Q(keywords__name=self.kwargs['slug'])|
            Q(keywords__name=self.kwargs['slug'])|Q(title__contains=self.kwargs['slug'])|
            Q(keywords__name__contains=self.kwargs['slug'])
        ).distinct()
        return context


class HomePageView(TemplateView):
    template_name = 'dictionary/index.html'


class SearchResultsView(ListView):
    model = Article
    template_name = 'dictionary/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Article.objects.filter(
            Q(keywords__name=query)|Q(title__contains=query)|Q(keywords__name__contains=query)
        ).distinct()
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context

