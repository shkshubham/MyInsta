from __future__ import absolute_import
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from braces import views
from django.contrib import messages
from posts.models import Post, Like
from posts.forms import CreatePostForm, UpdatePostForm
from posts.helpers import get_post

class DetailPostView(
    views.LoginRequiredMixin,
    generic.DetailView
):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super(DetailPostView, self).get_context_data(**kwargs)
        context['post'] = get_post(self.kwargs['slug'])
        return context

class CreatePostView(
    views.LoginRequiredMixin,
    generic.CreateView
):
    model = Post
    form_class = CreatePostForm
    template_name = 'form.html'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(CreatePostView, self).form_valid(form)

class UpdatePostView(
    views.LoginRequiredMixin,
    views.FormValidMessageMixin,
    generic.UpdateView
):
    model = Post
    form_valid_message = 'Successfully updated your post.'
    form_class = UpdatePostForm
    template_name = 'form.html'
    def get(self, request, *args, **kwargs):
        post = Post.objects.get(slug=kwargs['slug'])
        if (post.author != request.user):
            messages.warning(
                request,
                "You don't have permission to update this post"
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    'posts:view',
                    kwargs={ 'slug': kwargs['slug']})
            )
        else:
            return super(UpdatePostView, self).get(request, *args, **kwargs)


class DeletePostView(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.DeleteView
):
    model = Post
    form_valid_message = 'Successfully deleted your post.'
    success_url = reverse_lazy('home')
    template_name = 'delete.html'

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(slug=kwargs['slug'])

        if (post.author != request.user):
            messages.warning(
                request,
                'You don\'t have permission to delete this post.',
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    'posts:view',
                    kwargs={'slug': kwargs['slug']}
                )
            )
        else:
            return super(DeletePostView, self).get(request, *args, **kwargs)




@login_required
def like_post_view(request, *args, **kwargs):
    try:
        post = Post.objects.get(slug=kwargs['slug'])

        _, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            messages.warning(
                request,
                'You\'ve already liked the post.'
            )
    except Post.DoesNotExist:
        messages.warning(
            request,
            'Post does not exist'
        )

    return HttpResponseRedirect(
        reverse_lazy(
            'posts:view',
            kwargs={'slug': kwargs['slug']}
        )
    )

@login_required
def unlike_post_view(request, *args, **kwargs):
    try:
        like = Like.objects.get(
            post__slug=kwargs['slug'],
            user=request.user
        )
    except Like.DoesNotExist:
        messages.warning(
            request,
            'You didn\'t like the post.'
        )
    else:
        like.delete()

    return HttpResponseRedirect(
        reverse_lazy(
            'posts:view',
            kwargs={'slug': kwargs['slug']}
        )
    )