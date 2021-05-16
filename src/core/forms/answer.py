from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class AnswerFormSet(BaseInlineFormSet):
    def clean(self):
        if self.is_valid():
            super().clean()
            has_false = False
            has_true = False

            for answer in self.cleaned_data:
                if not answer:
                    continue
                if answer['is_true']:
                    has_true = True
                else:
                    has_false = True

            if not (has_true and has_false):
                raise ValidationError('Должен быть хотя бы один правильный ответ и один неправильный')
