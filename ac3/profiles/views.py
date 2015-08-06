from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib import messages
import django.views.generic as django_views
from django.contrib.auth import authenticate, login, logout
from movies.forms import RaterForm
from django.contrib.auth.decorators import login_required
from profiles.forms import ProfileForm, LoginForm, UserForm
from django.contrib.auth.models import User

# Create your views here.

def view_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            sometext = "You have sucessfully logged in, {}!".format(user.username)
            messages.add_message(request, messages.SUCCESS, sometext)
            return redirect('index')
        else:
            return render(request, "profiles/login.html",
                        {"failed": True, "username": username} )
    else:
        user_form = LoginForm()
        return render(request, "profiles/login.html", {'form':user_form})


def view_logout(request):
    user = request.user
    sometext = "You have sucessfully logged out. Bye."
    messages.add_message(request, messages.SUCCESS, sometext)
    logout(request)
    return redirect('/')
#    return redirect(reverse('index_view'))


def view_register(request):
    if request.method == "GET":
        user_form = UserForm()
        profile_form = ProfileForm()
        rater_form = RaterForm()
    elif request.method == "POST":
        user_form = UserForm(request.POST)
        rater_form = RaterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and rater_form.is_valid():
            user = user_form.save()
            rater = rater_form.save(commit=False)
            rater.user = user
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.age = rater.age
            profile.gender = rater.gender
            profile.save()
            rater.save()

            password = user.password
            # The form doesn't know to call this special method on user.
            user.set_password(password)
            user.save()

            # You must call authenticate before login. :(
            user = authenticate(username=user.username,
                                password=password)
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Congratulations, {}, on creating your new account! You are now logged in.".format(
                    user.username))
            return redirect('/')
    return render(request, "profiles/register.html", {'user_form': user_form,
                                                   'rater_form': rater_form})


@login_required
def edit_user(request):
    user = request.user
    if request.method == "GET":
        user_form = UserForm(instance=user)
    elif request.method == "POST":
        user_form = UserForm(instance=user, data=request.POST)
        if user_form.is_valid():
            n_user = user_form.save()
            password = user.password
            n_user.set_password(password)
            n_user.save()
            n_user = authenticate(username=n_user.username,
                                  password=password)
            login(request, n_user)
            messages.add_message(request, messages.SUCCESS,
                                 "Your profile has been updated!")
            return redirect('/')

    return render(request, "profiles/edit_user.html", {"form": user_form})


class ListUsersView(django_views.ListView):
    model = User
    template_name = "user_list.html"
    context_object_name='users'
    paginate_by=30


class UserDetailView(django_views.DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'this_user'
    the_user = None

    def dispatch(self, *args, **kwargs):
        self.the_user = User.objects.get(pk=kwargs['pk'])
        return super(UserDetailView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return User.objects.select_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = self.the_user.answer_set.all()
        context["questions"] = self.the_user.question_set.all()
        context["user"] = self.the_user
        context["score"] = (
            sum(num.score() for num in self.the_user.answer_set.all()) +
            (self.the_user.question_set.count() * 5) +
            (self.the_user.answerdownvote_set.count() * -1)
        )
        if self.the_user == self.request.user:
            context["is_self"] = True
        else:
            context["is_self"] = False

        return context
