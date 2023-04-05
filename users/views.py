from django.contrib.auth import authenticate, login
from users.forms import UserCreationForm, FollowForm
from django.views import View
from django.shortcuts import render, redirect
from users.models import Followers
from django.http import HttpResponseRedirect


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