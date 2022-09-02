from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.models import Member
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()

        Member.objects.create(user=instance)
        auth_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password1')
        )
        login(self.request, auth_user)

        return redirect(self.success_url)
