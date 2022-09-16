from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post

# Create your views here.


def home(request):
    cont = {"BOOKS": Post.objects.all()}
    return render(request, "webapp/home.html", cont)


class PostListView(ListView):
    model = Post
    template_name = "webapp/home.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "BOOKS"
    ordering = ["-date_posted"]


class PostDetailView(DetailView):
    model = Post
    # default template = <app>/<model>_<viewtype>.html


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about_(request):
    return render(request, "webapp/about.html", {"title": "about"})
