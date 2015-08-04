from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from movies.forms import UserForm, RaterForm, RatingForm, LoginForm
from django.contrib.auth.decorators import login_required
from profiles.forms import ProfileForm

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
