from . import views
from django.urls import path
from .views import HomePageView, SearchResultsView, KeywordsView, ArticleListView, ArticleDetailView, AuthorDetailView, \
    KeywordDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name="index"),
    path('article_list/', ArticleListView.as_view(), name="article_list"),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name="article_detail"),
    path('create/', views.create, name='create'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('author_list/', views.authorview, name='author_list'),
    path('author/<str:slug>/', AuthorDetailView.as_view(), name='author_detail'),
    path('keywords/', KeywordsView.as_view(), name="keywords"),
    path('keywords/<str:slug>/', KeywordDetailView.as_view(), name="keyword_detail"),

]