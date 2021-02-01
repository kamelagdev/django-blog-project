from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.db.models import Q

from .models import Post
from users.models import User
from .forms import CommentForm
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  DeleteView,
                                  UpdateView
                                  )


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(Q(title__icontains=query)).order_by('-date_posted')
        else:
            return self.model.objects.all().order_by('-date_posted')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['query']=self.request.GET.get('q')
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post_list.html'
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['query']=self.request.GET.get('q')
        return context


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comments = self.get_object().comments.all().order_by('-date_posted')
        context['comments'] = comments
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.get_object()
        form.save()
        return super(PostDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk':self.object.pk})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'content')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('title', 'content')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdateView, self).form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False
