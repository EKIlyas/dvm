from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView

from core.models import Cart, UserCart


class TestView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = 'core/test.html'
    queryset = Cart.objects.all()

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        obj = queryset.get(set__slug=self.kwargs.get('slug'), sequence=self.kwargs.get('sequence'))

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = self.get_object().answer_set.all()
        context.update({'answers': answers})

        return context

    def get(self, request, *args, **kwargs):
        current_cart = self.get_object()
        prev_cart = Cart.objects.get(set=current_cart.set,
                                     sequence=current_cart.sequence - 1) if current_cart.sequence > 1 else None

        if any([
            UserCart.objects.filter(user=request.user, cart=current_cart).count() != 0,
            (current_cart.sequence != 1) and (
                    UserCart.objects.filter(user=request.user, cart=prev_cart).count() == 0),
        ]):
            raise PermissionDenied()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST
        cart = self.get_object()
        is_correct_answer = True
        for answer in cart.answer_set.all():
            try:
                data[str(answer.id)]
                if not answer.is_true:
                    is_correct_answer = False
            except KeyError:
                if answer.is_true:
                    is_correct_answer = False

        user_cart = UserCart(user=request.user, cart=cart, is_true_answer=is_correct_answer)
        user_cart.save()

        try:
            Cart.objects.get(set=cart.set, sequence=cart.sequence + 1)
        except Cart.DoesNotExist:
            set_obj = cart.set
            set_obj.have_result = True
            set_obj.save()

            return HttpResponseRedirect(reverse('core:result', args=(cart.set.slug,)))

        return HttpResponseRedirect(reverse('core:test', args=(cart.set.slug, cart.sequence + 1,)))
