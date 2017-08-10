from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from braces import views
from posts.helpers import get_posts
from .models import User, Connection
from .forms import SignUpForm, UpdateAccountForm, LoginForm, ChangePasswordForm
from .helpers import get_current_user
from django.http import JsonResponse


class DetailAccountView(
        views.LoginRequiredMixin,
        generic.DetailView
):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'account_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailAccountView, self).get_context_data(**kwargs)
        username = self.kwargs['username']
        context['username'] = username
        context['posts'] = get_posts(username)
        context['user'] = get_current_user(self.request)
        context['following'] = Connection.objects.filter(
            follower__username=username).count()
        context['followers'] = Connection.objects.filter(
            following__username=username).count()

        if username is not context['user'].username:
            result = Connection.objects.filter(
                follower__username=context['user'].username
            ).filter(
                following__username=username
            )

            context['connected'] = True if result else False

        return context



class LoginView(views.AnonymousRequiredMixin, generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'form.html'
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password = password)
        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class UpdateAccountView(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        generic.UpdateView
):
    model = User
    form_valid_message = 'Successfully updated your account.'
    form_class = UpdateAccountForm
    template_name = 'form.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'



class SignUpView(
        views.AnonymousRequiredMixin,
        views.FormValidMessageMixin,
        generic.CreateView
):
    model = User
    form_class = SignUpForm
    form_valid_message = 'Successfully created your account, ' \
                         'go ahead and login.'
    success_url = reverse_lazy('accounts:login')
    template_name = 'form.html'


@login_required
def LogoutView(request):
    logout(request)
    messages.success(request, 'You\'ve been logged out. Come back soon!')
    return HttpResponseRedirect(reverse_lazy('home'))



class FollowersListView(
        views.LoginRequiredMixin,
        generic.ListView
):
    model = Connection
    template_name = 'connections_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        username = self.kwargs['username']
        return Connection.objects.filter(following__username=username)

    def get_context_data(self):
        context = super(FollowersListView, self).get_context_data()
        context['mode'] = 'followers'
        return context

class FollowingListView(
        views.LoginRequiredMixin,
        generic.ListView
):
    model = Connection
    template_name = 'connections_list.html'
    context_object_name = 'users'
    def get_queryset(self):
        username = self.kwargs['username']
        return Connection.objects.filter(follower__username=username)

    def get_context_data(self):
        context = super(FollowingListView, self).get_context_data()
        context['mode'] = 'following'
        return context

class ListAccountView(
        views.LoginRequiredMixin,
        generic.ListView
):
    model = User
    template_name = 'account_list.html'
    context_object_name = 'users'

@login_required
def follow_view(request, *args, **kwargs):
    try:
        follower = User.objects.get(username=request.user)
        following = User.objects.get(username=kwargs['username'])
    except User.DoesNotExist:
        messages.warning(
            request,
            '{} is not a registered user.'.format(kwargs['username'])
        )
        return HttpResponseRedirect(reverse_lazy('home'))

    if follower == following:
        messages.warning(
            request,
            'You cannot follow yourself.'
        )
    else:
        _, success = Connection.objects.get_or_create(
            follower=follower,
            following=following
        )

        if (success):
            messages.success(
                request,
                'You\'ve successfully followed {}.'.format(following.username)
            )
        else:
            messages.warning(
                request,
                'You\'ve already followed {}.'.format(following.username)
            )
    return HttpResponseRedirect(
        reverse_lazy(
            'accounts:profile',
            kwargs={'username': following.username}
        )
    )

@login_required
def unfollow_view(request, *args, **kwargs):
    try:
        follower = User.objects.get(username=request.user)
        following = User.objects.get(username=kwargs['username'])

        if follower == following:
            messages.warning(
                request,
                'You cannot unfollow yourself.'
            )
        else:
            unfollow = Connection.objects.get(
                follower=follower,
                following=following
            )

            unfollow.delete()

            messages.success(
                request,
                'You\'ve just unfollowed {}.'.format(following.username)
            )
    except User.DoesNotExist:
        messages.warning(
            request,
            '{} is not a registered user.'.format(kwargs['username'])
        )
        return HttpResponseRedirect(reverse_lazy('home'))
    except Connection.DoesNotExist:
        messages.warning(
            request,
            'You didn\'t follow {0}.'.format(following.username)
        )

    return HttpResponseRedirect(
        reverse_lazy(
            'accounts:profile',
            kwargs={'username': following.username}
        )
    )


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = username + 'already exists.'
    return JsonResponse(data)
