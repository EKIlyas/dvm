from django.contrib import admin
from .forms import AnswerFormSet
from .models import Cart, Set, Answer
from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline


class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 1
    formset = AnswerFormSet
    fields = ['text', 'is_true']


class CartInline(NestedStackedInline):
    model = Cart
    fields = ['question']
    inlines = [AnswerInline]

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


@admin.register(Set)
class SetAdmin(NestedModelAdmin):
    inlines = [CartInline]
    fields = ['name']
    view_on_site = False
