from django.contrib import admin

# Register your models here.
from .models import (
    Hsk,  Keyword, GrammarTopic,
    Textbook, Lesson, Article, Assignment, RatingStar,
    Rating, Comment, Course, Quiz
)

admin.site.register(Hsk)
admin.site.register(Keyword)
admin.site.register(GrammarTopic)
admin.site.register(Textbook)
admin.site.register(Lesson)
admin.site.register(Article)
admin.site.register(Assignment)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(Comment)
