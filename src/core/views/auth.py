from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('core:sets')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid
