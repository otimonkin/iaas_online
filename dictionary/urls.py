from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name='about'),
    path('create', views.create, name='create'),
    path('author_list', views.authorview, name='author_list'),
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name="article_detail")
]