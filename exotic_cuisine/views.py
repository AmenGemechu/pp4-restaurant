from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
#
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm, CreateUserForm
from django.contrib import messages
# from .model import exotic_cuisine
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# class RestrictedView(LoginRequiredMixin, TemplateView):
#    template_name = 'index.html'


# @login_required(login_url='login')

class PostList(LoginRequiredMixin, generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by(
        '-created_on')    # latest post on top
    template_name = 'index.html'
    paginate_by = 6  # max_post per page


class PostDetail(LoginRequiredMixin, View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(LoginRequiredMixin, View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('exotic_cuisine:post_detail', args=[slug]))


class ArticleDetailView(PostDetail):
    model = Post
    template_name = 'article_details.html'


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'add_post.html'
    # fields = '__all__'
    success_url = reverse_lazy('exotic_cuisine:posts')
    fields = ('title', 'content', 'featured_image')


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ('title', 'content', 'featured_image')
    # pk_url_kwarg = 'pk'
    # success_url = reverse_lazy('exotic_cuisine:posts')

    """
    Ristrict profile edit
    """

    def test_func(self):
        return self.get_object().author_id == self.request.user.pk

    def handle_no_permission(self):
        return redirect('/')

    # def test_func(self):
    #    if self.get_object().author_id == self.request.user.pk:
    #        return True
    #    else:
    #        return redirect('/')
        # return False

    # def get_queryset(self, *args, **kwargs):
    #    return super().get_queryset(*args, **kwargs).filter(
    #        author=self.request.user
    #    )


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # pk_url_kwarg = 'pk'
    template_name = "delete_post.html"
    # success_url = reverse_lazy('exotic_cuisine:home')

    """
    Ristrict post delete
    """

    def test_func(self):
        return self.get_object().author_id == self.request.user.pk

    def handle_no_permission(self):
        return redirect('/')


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
            # Redirect to a success page.

        else:
            # Return an 'invalid login' error message.
            messages.success(
                request, "There was an Error Logingin. Try again..")
            return redirect('exotic_cuisine:login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You are Logged Out!"))
    return redirect('exotic_cuisine:login')


# Single post
# class SingleView(DeleteView):
#    model = exotic_cuisine
#    template_name = 'single.html'
#    context_object_name = 'post'


# class PostsView(ListView):
#    model = exotic_cuisine
#    template_name = 'posts.html'
#    context_object_name = 'post_list'


# class AddView(CreateView):
#    model = exotic_cuisine
#    template_name = "add.html"
#    fields = '__all__'
#    success_url = reverse_lazy('exotic_cuisine:posts')


# def home(request):
#    form = CreateUserForm()

#    if request.method == 'POST':
#        form = CreateUserForm(request.POST)
#        if form.is_valid():
#            form.save()
    # return redirect('login')

#    context = {'form': form}
#    return render(request, 'register.html', context)


# HomeView
# @login_required
# def home(request):
#    model = Post
#    template_name = 'index.html'
#    context_object_name = 'index'
