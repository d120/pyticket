from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import LoginForm, SettingsForm
from django.utils.translation import ugettext_lazy as _


class LoginView(View):
    """ Backend for the login template in login.html """
    template_login = "login.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return forward_if_authenticated(self.request)

        next = None
        if "next" in self.request.GET:
            next = self.request.GET.get("next")

        form = LoginForm()

        content = {
            "form": form,
            "next": next
        }
        return render(self.request, self.template_login, content)

    def post(self, *args, **kwargs):
        # create a form instance and populate it with data from the request:
        form = LoginForm(self.request.POST)

        next = None
        if "next" in self.request.GET:
            next = self.request.GET.get("next")

        if form.is_valid():
            user = form.login(self.request)
            if user is not None:
                login(self.request, user)
                return forward_if_authenticated(self.request)

        content = {
            "form": form,
            "next": next
        }
        return render(self.request, self.template_login, content)


class LogoutView(View):
    """ Backend for the logout template in logout.html """

    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('dashboard'))

    def post(self, *args, **kwargs):
        pass


class SettingsView(LoginRequiredMixin, View):
    """ Backend for the settings template in settings.html """
    template_settings = "settings.html"

    def get(self, *args, **kwargs):
        user = self.request.user

        form = SettingsForm(
            {'sending_email_once_a_day': user.sending_email_once_a_day})

        content = {
            "form": form
        }

        return render(self.request, self.template_settings, content)

    def post(self, *args, **kwargs):
        user = self.request.user
        form = SettingsForm(self.request.POST)

        if form.is_valid():
            # Enables daily summary email
            user.sending_email_once_a_day = form.cleaned_data[
                "sending_email_once_a_day"]
            user.save()
            messages.success(self.request,
                             _('Einstellungen wurden erfolgreich übernommen!'))
        else:
            messages.error(self.request,
                           _('Die Einstellung konnte nicht übernommen werden!'))

        content = {
            "form": form
        }

        return render(self.request, self.template_settings, content)


def forward_if_authenticated(request):
    """
    If the user is logged in successfully he will be forwarded to the page he
    tried to access. If no page exists he will be forwarded to dashboard
    :param request: Contains metadata about the request
    :return: redirect to the corresponding page
    """
    if "next" in request.POST:
        return HttpResponseRedirect(request.POST.get('next'))
    elif "next" in request.GET:
        return HttpResponseRedirect(request.GET.get('next'))
    else:
        return HttpResponseRedirect(reverse('dashboard'))
