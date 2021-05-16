from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from core.models import Set, UserCart


class SetView(LoginRequiredMixin, ListView):
    model = Set
    template_name = 'core/sets.html'

    def post(self, request, *args, **kwargs):
        set_ = Set.objects.get(name=request.POST.get('next'))
        UserCart.objects.filter(user=request.user, cart__set=set_).delete()
        return HttpResponseRedirect(reverse('core:test', args=(set_.slug, 1)))
