from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django_htmx.http import HttpResponseClientRedirect

from accounts.forms import SignInForm, SignUpForm


@method_decorator([login_not_required], name='dispatch')
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'sign_up.html'

    def get(self, request: HttpRequest):
        context = {
            'form': self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not form.is_valid():
            context = {'form': form}
            return render(request, 'partials/form.html', context)

        form.save()

        login(request, form.instance)

        return HttpResponseClientRedirect(reverse('dashboard'))


@method_decorator([login_not_required], name='dispatch')
class SignInView(View):
    form_class = SignInForm
    template_name = 'sign_in.html'

    def get(self, request: HttpRequest):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)

        if not form.is_valid():
            context = {'form': form}
            return render(request, 'partials/form.html', context)

        login(request, form.user)

        return HttpResponseClientRedirect(reverse('dashboard'))
