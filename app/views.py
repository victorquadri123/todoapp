from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm



# Create your views here.

def landing(request):

    return render(request, "todo.html")


def register(request):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)
        

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            user_obj = User(username = username, email = email, password = password )
            user_obj.set_password(password)

            return redirect("app:signin")
        


    
    context = {
        "form": form
    }

    return render(request, "signup.html", context)


def login_attepmt(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        

        UserObject = User.objects.filter(username= username).first()

        if UserObject is None:
            messages.error(request,"we can't find this account")
            return redirect("app:register")
        
        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(request, "wrong paassword")
            return redirect("app:signin")
        
        login(request,user)
        return redirect("app:home")
    


    return render(request, "signin.html")

def home (request):

    return render(request, "index.html")






