from django.shortcuts import render, redirect
from django.views.generic.base import View
from blog.models import Post, Like, Reviews, Tags, Reviews_like
from django.contrib.auth.models import AnonymousUser
from blog.forms import LikeForm, PostForm, CommentForm, LikeReviewForm
from users.models import User, Followers
from django.db.models import Count
from django.http import HttpResponseRedirect


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
    
    def get_single_review_data(self, review):
        likes = Reviews_like.objects.filter(review=review)
        reviews_data = {
            # модифицируем если надо что-то добавить в инфо про пост
            'review_data': review,
            'likes': likes,
            'user_likes': [i['user'] for i in Reviews_like.objects.values('user').filter(review=review)],
        }
        return reviews_data
    
    def get_single_post_data(self, post):
        likes = Like.objects.filter(post=post)
        comments = Reviews.objects.filter(post=post)
        post_data = {
            # модифицируем если надо что-то добавить в инфо про пост
            'post_data': post,
            'likes': likes,
            'comments': comments,
            'user_likes': [i['user'] for i in Like.objects.values('user').filter(post=post)],
        }
        return post_data
    
    def get_data(self):
        # контекст страницы
        context = {
            'top_tags': self.get_top_tags(count=6),
            'top_users': self.get_top_followers(),
            'get_following': self.get_following() if self.request.user!=self.anonimys else None,
        }
        return context
    
    def get(self, request, **kwargs):
        if 'slug' in kwargs:
            context = self.get_data(kwargs.get('slug'))
        elif 'pk' in kwargs:
            context = self.get_data(kwargs.get('pk'))
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
    template_name = "blog/viewer_list.html"

    def get_data(self):
        context = super().get_data()

        post_queryset = Post.objects.annotate(num_likes=Count('post_by_likes')).filter(draft=False).order_by('-num_likes', '-date')
        posts_data = self.get_post_data(post_queryset)

        # контекст страницы
        context.update({
            'posts_list': posts_data,
            'page_name': 'Hot feeds'
        })

        return context
    
class ExploreList(Posts_list_base):
    template_name = "blog/viewer_list.html"

    def get_data(self):
        context = super().get_data()

        post_queryset = Post.objects.filter(draft=False).order_by('-date')
        posts_data = self.get_post_data(post_queryset)

        # контекст страницы
        context.update({
            'posts_list': posts_data,
            'page_name': 'Explore'
        })

        return context

class TagPost(Posts_list_base):
    template_name = "blog/post_list_tags.html"

    def get_data(self, pk):
        context = super().get_data()

        post_queryset = Post.objects.filter(draft=False, tag__id=pk).order_by("-date")
        tag = Tags.objects.get(id=pk)
        posts_data = self.get_post_data(post_queryset)

        # окнтекст страницы
        context.update({
            'posts_list': posts_data,
            'page_name': tag.text.capitalize()
        })

        return context
    

class PostPage(Posts_list_base):
    template_name = "blog/post_page.html"

    def get_reviews_list(self, pk):
        reviews = list()
        treads = Reviews.objects.filter(post__id=pk, parent=None, tread=None)
        for tread in treads:
            reviews.append(
                {
                    'review': self.get_single_review_data(tread),
                    'sub_reviews': [self.get_single_review_data(i) for i in Reviews.objects.filter(tread__id=tread.id).order_by("date")],
                }
            )
        return reviews

    def get_data(self, pk):
        context = super().get_data()
        post_queryset = Post.objects.get(id=pk)
        posts_data = self.get_single_post_data(post_queryset)

        # окнтекст страницы
        context.update({
            'post': posts_data,
            'page_name': post_queryset.title.capitalize(),
            'reviews': self.get_reviews_list(pk),
        })

        return context
    


class SearchData(Posts_list_base):
    template_name = "blog/search.html"

    def get_data(self):
        context = super().get_data()

        search_data = self.request.GET.get('q')

        post_queryset = Post.objects.filter(draft=False, title__icontains=search_data).order_by("-date")
        topic_queryset = Tags.objects.annotate(post_count=Count('tag_post')).filter(text__icontains=search_data).order_by('-post_count')
        profile_queryset = User.objects.annotate(followers_count=Count('followers')).filter(username__icontains=search_data).order_by('-followers_count')
        posts_data = self.get_post_data(post_queryset)


        context.update({
            'search_post_list': posts_data if posts_data else None,
            'search_topic_list': topic_queryset if topic_queryset else None,
            'search_profile_list': profile_queryset if profile_queryset else None,
            'page_name': search_data[:10].capitalize()
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

         # Получить URL, с которого был выполнен запрос
        referer_url = request.META.get('HTTP_REFERER')

        # Проверить, что URL внутри домена вашего приложения
        if referer_url and referer_url.startswith(request.build_absolute_uri('/')[:-1]):
            return HttpResponseRedirect(referer_url)
        else:
            return redirect('home')


class LikeReview(View):
    anonimys = AnonymousUser()

    def post(self, request):
        form = LikeReviewForm(request.POST)
        if form.is_valid() and request.user != self.anonimys:
            review = form.cleaned_data.get('review')
            likes = Reviews_like.objects.filter(review=review)
            if request.user in [like.user for like in likes]:
                obj = Reviews_like.objects.get(review=form.cleaned_data.get('review'), user=request.user)
                obj.delete()
            else:
                form = form.save(commit=False)
                form.user = request.user
                form.save()

         # Получить URL, с которого был выполнен запрос
        referer_url = request.META.get('HTTP_REFERER')

        # Проверить, что URL внутри домена вашего приложения
        if referer_url and referer_url.startswith(request.build_absolute_uri('/')[:-1]):
            return HttpResponseRedirect(referer_url)
        else:
            return redirect('home')


class Terms(View):
    template_name = "blog/terms.html"

    def get(self, request):
        context = {
            'page_name': 'Terms of use',
            'page_subname': '5 minute read'
        }
        return render(request, self.template_name, context)

class AddPost(View):
    template_name = "blog/post_create.html"

    def get(self, request):
        context = {
            'page_name': 'Create a post',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()

            # Get list of selected tags from select element
            selected_tags = request.POST.getlist('tag')

            # Create and save Tag objects for each selected value
            for tag_text in selected_tags:
                tag, created = Tags.objects.get_or_create(text=tag_text)
                post.tag.add(tag)
        return redirect('home')
    

class AddComment(View):
    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.owner = request.user
            review.save()

        referer_url = request.META.get('HTTP_REFERER')

        # Проверить, что URL внутри домена вашего приложения
        if referer_url and referer_url.startswith(request.build_absolute_uri('/')[:-1]):
            return HttpResponseRedirect(referer_url)
        else:
            return redirect('home')