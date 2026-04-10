from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SignupForm
from .models import Dish, Account

# Create your views here.

def login_form(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        account = Account.objects.filter(username=username, password=password).first()
        if account:
            request.session['account_id'] = account.pk
            return redirect('basic_list', pk=account.pk)
        else:
            error_message = "Invalid Credentials"
    return render(request, 'tapasapp/login.html', {'error': error_message})

def signup_form(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            account = form.save()  # saves username + password
            request.session['account_id'] = account.pk
            messages.success(request, "Account created successfully")
            return redirect('login_form')
    else:
        form = SignupForm()
    return render(request, 'tapasapp/signup.html', {'form': form})      

def better_menu(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/better_list.html', {'dishes': dish_objects})

def add_menu(request):
    if request.method == "POST":
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('better_menu')
    else:
        return render(request, 'tapasapp/add_menu.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')

def update_dish(request, pk):
    if request.method == "POST":
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d': d})
    
def basic_list(request, pk):
    account = get_object_or_404(Account, pk=pk)
    items = Dish.objects.all() 
    return render(request, "tapasapp/basic_list.html", {"items": items, "account": account})

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, "tapasapp/manage_account.html", {"account": account})

def logout_view(request):
    
    request.session.flush()
    messages.info(request, "You have been logged out")
    return redirect("login_form")
