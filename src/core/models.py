from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Set(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Набор'
        verbose_name_plural = 'Наборы Тестов'

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)


class Cart(models.Model):
    set = models.ForeignKey(Set, verbose_name='Набор', on_delete=models.CASCADE)
    question = models.CharField('Вопрос', max_length=400)
    sequence = models.PositiveSmallIntegerField('Порядок')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.sequence:
            prev_cart = Cart.objects.filter(set=self.set).order_by('-sequence').first()
            if prev_cart:
                self.sequence = prev_cart.sequence + 1
            else:
                self.sequence = 1
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Answer(models.Model):
    text = models.CharField('Текст', max_length=500)
    is_true = models.BooleanField('Верный', default=False)
    cart = models.ForeignKey(Cart, verbose_name='Карточка', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cart.question}: {self.text}"

    class Meta:
        verbose_name = 'Вариант Ответа'
        verbose_name_plural = 'Варианты Ответов'


class UserCart(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Карточка', on_delete=models.CASCADE)
    is_true_answer = models.BooleanField('Правильность Ответа', default=False)
