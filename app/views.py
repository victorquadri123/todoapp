from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Todo



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
        

        UserObject = User.objects.filter(username=username).first()

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

@login_required
def home (request):
    CurrentDate = timezone.now()
    CurrentDate = CurrentDate.strftime("%Y-%m-%d")
    currenttime = timezone.now()+timedelta(hours=6, minutes=6)
    currenttime = currenttime.strftime("%H:%M")
    context = {"success": False , "currenttime": currenttime, "currentdate": CurrentDate}
    status = "pending"

    if request.method == "POST":
        title = request.POST("title")
        description = request.POST("description")
        duedate = request.POST("duedate")
        duetime = request.POST("duetime")
        important = request.POST.get("important")
        
        duedatetime = datetime.strptime(f"{duedate} {duetime}", '%Y-%m_%d %H:%M' )
        min_due_date_time = timezone.now()+timedelta(minutes=5)
        duedatetime = timezone.make_aware(duedatetime, timezone.get_current_timezone())
        

        if duedatetime <= min_due_date_time:
            messages.error(request, f"due time must at least 5 minutes from now")
            duedatetime = timezone.now()+timedelta(minutes=5)

        task = Todo(
            TaskTitle = title,
            Description = description,
            DueDate = duedate,
            Important = bool(important),
            Status = "overdue" if duedatetime < timezone.now() else status,
            user = request.user
            
        )
        task.save()
        context["success"] = True
        
    all_task = Todo.objects.filter(user = request.user)  
    context["running_task"] = all_task



        
    return render(request, "index.html")

def logout_view(request):
    logout(request)
    return redirect('/')






