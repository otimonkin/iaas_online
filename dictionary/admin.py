from django.contrib import admin

# Register your models here.
from .models import (
    Hsk,  Keyword, GrammarTopic,
    Textbook, Lesson, Article, Assignment, RatingStar,
    Rating, Comment, Course, Quiz
)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "draft")
    search_fields = ("keywords__name", "title")
    list_editable = ("draft",)


@admin.register(Keyword)
class KeywordsAdmin(admin.ModelAdmin):
    list_display = ("name", "hsk")


admin.site.register(Hsk)
admin.site.register(GrammarTopic)
admin.site.register(Textbook)
admin.site.register(Lesson)
admin.site.register(Assignment)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(Comment)
