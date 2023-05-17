from django.contrib.auth import authenticate, login
from users.forms import UserCreationForm, FollowForm
from django.views import View
from django.shortcuts import render, redirect
from users.models import Followers
from django.http import HttpResponseRedirect
from .forms import ProfileSettingsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMessage


# Create your views here.
class Register(View):

    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

# как вариант можно сделать один класс и один роут (если данный юзер уже подписан на этого юзера, то отписаться)
class Follow(View):
    def post(self, request):
        form = FollowForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
        # Получить URL, с которого был выполнен запрос
        referer_url = request.META.get('HTTP_REFERER')

        # Проверить, что URL внутри домена вашего приложения
        if referer_url and referer_url.startswith(request.build_absolute_uri('/')[:-1]):
            return HttpResponseRedirect(referer_url)
        else:
            return redirect('home')

class Unfollow(View):
    def post(self, request):
        form = FollowForm(request.POST)
        if form.is_valid():
            obj = Followers.objects.get(follow_by=form['follow_by'].data, owner=request.user)
            obj.delete()
        # Получить URL, с которого был выполнен запрос
        referer_url = request.META.get('HTTP_REFERER')

        # Проверить, что URL внутри домена вашего приложения
        if referer_url and referer_url.startswith(request.build_absolute_uri('/')[:-1]):
            return HttpResponseRedirect(referer_url)
        else:
            return redirect('home')
        


@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            
            referer_url = request.META.get('HTTP_REFERER')

            # Проверить, что URL внутри домена вашего приложения
            if referer_url and referer_url.startswith(request.build_absolute_uri('/')[:-1]):
                return HttpResponseRedirect(referer_url)
            else:
                return redirect('home')
    else:
        form = ProfileSettingsForm(instance=request.user)
    return render(request, 'profile/settings.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html' # ваш собственный шаблон формы для ввода email
    html_email_template_name = 'registration/password_reset_email.html'
    success_url = '/' # страница, на которую пользователь будет перенаправлен после отправки письма

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Отправка HTML-письма.
        """
        subject = self.render_subject(subject_template_name, context)
        # Генерация текстового содержимого письма
        email_message = self.render_mail(email_template_name, context)

        if html_email_template_name is not None:
            # Генерация HTML-содержимого письма
            html_email = self.render_mail(html_email_template_name, context)
            # Установка типа содержимого письма как HTML
            email_message.content_subtype = "html"
            # Добавление HTML-содержимого в письмо
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # добавьте дополнительные данные для контекста, если это необходимо
        return context