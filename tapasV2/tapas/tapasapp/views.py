from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import SignupForm
from .models import Dish, Account

# Create your views here.

def login_form(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            account, created = Account.objects.get_or_create(user=user)
            return redirect('basic_list', pk = account.pk)
        else:
            error_message = "Invalid Credentials"
    return render(request, 'tapasapp/login.html', {'error': error_message})

def signup_form(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username = username, password = password)
            Account.objects.create(user = user)
            login(request, user)
            return redirect('login_form')
    else:
        form = SignupForm()
    return render(request, 'tapasapp/signup.html', {'form':form})    

@login_required
def better_menu(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/better_list.html', {'dishes': dish_objects})

@login_required
def add_menu(request):
    if request.method == "POST":
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(account = request.user.account, name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('better_menu')
    else:
        return render(request, 'tapasapp/add_menu.html')

@login_required
def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

@login_required
def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')

@login_required
def update_dish(request, pk):
    if request.method == "POST":
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d': d})

@login_required
def basic_list(request, pk):
    account = get_object_or_404(Account, pk=pk)
    items = Dish.objects.all() 
    return render(request, "tapasapp/basic_list.html", {"items": items, "account": account})

@login_required
def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, "tapasapp/manage_account.html", {"account": account})

@login_required
def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    user = account.user

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect")
            return redirect('change_password', pk=pk)
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match")
            return redirect('change_password', pk=pk)
        user.set_password(new_password)
        user.save()
        messages.success(request, "Password updated successfully")
        return redirect('login_form')
    return render(request, "tapasapp/change_password.html", {"account": account})

@login_required    
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    user = account.user
    user.delete()
    request.session.flush()
    messages.info(request, "Your account has been deleted")
    return redirect('login_form')

@login_required
def logout_view(request):
    
    request.session.flush()
    messages.info(request, "You have been logged out")
    return redirect("login_form")
