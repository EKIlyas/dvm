from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from core.models import UserCart


class ResultView(LoginRequiredMixin, TemplateView):
    template_name = 'core/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_answers = UserCart.objects.filter(user=self.request.user, cart__set__slug=self.kwargs.get('slug'))
        all_count = user_answers.count()
        correct_count = user_answers.filter(is_true_answer=True).count()
        not_correct_count = all_count-correct_count
        result = {
            'not_correct_count': not_correct_count,
            'correct_count': correct_count,
            'percent': 0 if correct_count == 0 else round(correct_count*100/all_count, 2),
        }
        context.update(result)

        return context
