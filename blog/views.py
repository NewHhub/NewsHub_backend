from django.shortcuts import render, redirect
from django.views.generic.base import View
from blog.models import Post, Like, Reviews, Tags
from django.contrib.auth.models import AnonymousUser
from blog.forms import LikeForm
from users.models import User, Followers
from django.db.models import Count

class Posts_list_base(View):
    anonimys = AnonymousUser()

    # топ 5 пользователей по кол-ву кодписчиков
    def get_top_followers(self, count=5):
        return User.objects.annotate(followers_count=Count('followers')).all().order_by('-followers_count')[:count]

    # получить всех подписчиков пользователя
    def get_following(self):
        followers = Followers.objects.filter(owner=self.request.user)
        list_follow = list()
        for follower in followers:
            list_follow.append(follower.follow_by)
        return list_follow

    def get_top_tags(self, count):
        querry = Tags.objects.annotate(post_count=Count('tag_post')).all().order_by('-post_count')[:count]
        return querry

    def get_post_data(self, queryset):
        data = list()
        for post in queryset:
            likes = Like.objects.filter(post=post)
            comments = Reviews.objects.filter(post=post)
            post_data = {
                # модифицируем если надо что-то добавить в инфо про пост
                'post_data': post,
                'likes': likes,
                'comments': comments,
                'user_likes': [i['user'] for i in Like.objects.values('user').filter(post=post)],
            }
            data.append(post_data)
        return data
    
    def get_data(self):
        # контекст страницы
        context = {
            'top_tags': self.get_top_tags(count=3),
            'top_users': self.get_top_followers(),
            'get_following': self.get_following() if self.request.user!=self.anonimys else None,
        }
        return context
    
    def get(self, request, **kwargs):
        if 'slug' in kwargs:
            context = self.get_data(kwargs.get('slug'))
        else:
            context = self.get_data()
        return render(request, self.template_name, context)


class PostsList(Posts_list_base):
    template_name = "blog/post_list.html"
    
    def get_data(self):
        context = super().get_data()

        if self.request.user!=self.anonimys:
            following_users = [f.follow_by for f in self.request.user.following.all()]
        else:
            following_users = None
        

        # в запросе мы не встретим посты если мы авторизированы и при этом не подписаны не на кого
        if self.request.user!=self.anonimys and following_users:
            # если человек авторизирован, то нужно выводить только тех на кого он подписан (себя выводить не стоит)
            post_queryset = Post.objects.filter(owner__in=following_users, draft=False).order_by('-date')
        elif self.request.user!=self.anonimys and not following_users:
            # ненужно делать запрос на посты если мы не на кого не подписаны
            post_queryset = list()
        else:
            # если человек аноним, выводим все посты всех пользователей (кторые активные)
            post_queryset = Post.objects.filter(draft=False).order_by('-date')

        # контекст страницы
        context.update({
            'top_users_if_no_followers': None if following_users else self.get_top_followers(count=6),
            'posts_list': self.get_post_data(post_queryset),
            'page_name': 'Home page'
        })

        return context


class HotList(Posts_list_base):
    template_name = "blog/hot_list.html"

    def get_data(self):
        context = super().get_data()

        post_queryset = Post.objects.annotate(num_likes=Count('post_by_likes')).filter(draft=False).order_by('-num_likes')
        posts_data = self.get_post_data(post_queryset)

        # контекст страницы
        context.update({
            'posts_list': posts_data,
            'page_name': 'Hot feeds'
        })

        return context

class TagPost(Posts_list_base):
    template_name = "blog/post_list_tags.html"

    def get_data(self, slug):
        context = super().get_data()

        post_queryset = Post.objects.filter(draft=False, tag__text=slug).order_by("-date")
        posts_data = self.get_post_data(post_queryset)

        # окнтекст страницы
        context.update({
            'posts_list': posts_data,
            'page_name': slug.capitalize()
        })

        return context


class LikePost(View):
    anonimys = AnonymousUser()

    def post(self, request):
        form = LikeForm(request.POST)
        if form.is_valid() and request.user != self.anonimys:
            post = form.cleaned_data.get('post')
            likes = Like.objects.filter(post=post)
            if request.user in [like.user for like in likes]:
                obj = Like.objects.get(post=form.cleaned_data.get('post'), user=request.user)
                obj.delete()
            else:
                form = form.save(commit=False)
                form.user = request.user
                form.save()
        return redirect('home')


class Terms(View):
    template_name = "blog/terms.html"

    def get(self, request):
        context = {
            'page_name': 'Terms of use',
            'page_subname': '5 minute read'
        }
        return render(request, self.template_name, context)