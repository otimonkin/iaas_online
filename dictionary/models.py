from django.db import models
from django.urls import reverse

from users.models import User


class Hsk(models.Model):
    """ Уровень HSK """
    value = models.PositiveSmallIntegerField("Уровень", default=1)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = "Уровень HSK"
        verbose_name_plural = "Уровни HSK"


class Keyword(models.Model):
    name = models.CharField("Ключевое слово", max_length=100)
    hsk = models.ForeignKey(Hsk, related_name="hsk_level", on_delete=models.CharField)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"


class GrammarTopic(models.Model):
    title = models.CharField("Тема", max_length=100)
    hsk = models.ForeignKey(Hsk, related_name="hsk_grammar_level", on_delete=models.CharField)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Textbook(models.Model):
    title = models.CharField("Название", max_length=250)
    authors = models.ManyToManyField(User, related_name="textbook_author", blank=True)  # нужно ли verbose_name= ??
    image = models.ImageField

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Учебное пособие"
        verbose_name_plural = "Учебные пособия"


class Lesson(models.Model):    # Разные учебники, порядковы номер в каждом ??
    textbook = models.ForeignKey(Textbook, verbose_name="Учебник", on_delete=models.CharField)
    value = models.SmallIntegerField("Номер урока", default=0)
    grammar = models.ManyToManyField(GrammarTopic, verbose_name="грамматические темы", related_name="lesson_grammar")

    def __str__(self):
        return f'{self.textbook} - {self.value}'

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Article(models.Model):
    title = models.CharField("Заголовок", max_length=250)
    message = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)
    keywords = models.ManyToManyField(Keyword, verbose_name="Ключевые слова", related_name="article_keywords")
    grammar = models.ManyToManyField(GrammarTopic, verbose_name="Грамматика", related_name="article_grammar", blank=True)
    lessons = models.ManyToManyField(Lesson, verbose_name="Уроки", related_name="article_lesson", blank=True)
    authors = models.ManyToManyField(User, verbose_name="Автор", related_name="article_author")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={"slug": self.url})


    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class Assignment(models.Model):
    lessons = models.ManyToManyField(Lesson, verbose_name="Урок", related_name="assignment_lesson")
    number = models.PositiveSmallIntegerField("Номер предложения", blank=True)
    text = models.CharField("Задание на перевод", max_length=300)
    solution = models.CharField("Ответ", max_length=300)
    best_solution = models.CharField("Оптимальный вариант", max_length=300)
    grammar = models.ManyToManyField(GrammarTopic, verbose_name="Грамматика", related_name="assignment_grammar", blank=True)
    keywords = models.ManyToManyField(Keyword, verbose_name="Ключевые слова", related_name="assignment_keywords", blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Предложение на перевод"
        verbose_name_plural = "Педложения на перевод"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(models.Model):
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Статья")  # Почему on_delete=models.Charfield ?
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")  # Может ли райтинг быть и у статьи и у автора?(среднее по всем статьям)

    def __str__(self):
        return self.star

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Comment(models.Model):
    """Комментарии к статьям"""
    name = models.CharField("Имя", max_length=100)  # Только зарегистрированные?
    text = models.TextField("Комментарий", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    article = models.ForeignKey(Article, verbose_name="Статья", on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.name} - {self.article}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Quiz(models.Model):
    name = models.CharField("Название теста", max_length=100)
    assignments = models.ManyToManyField(Assignment, verbose_name="Предложения на перевод", related_name="quiz_assignments")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Course(models.Model):
    name = models.CharField("Курс", max_length=100)
    students = models.ManyToManyField(User, verbose_name="Студенты", related_name="course_student")
    mentor = models.ManyToManyField(User, verbose_name="Ментор", related_name="course_mentor")
    assignment = models.ManyToManyField(Assignment, verbose_name="Задание", related_name="course_assignment")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"