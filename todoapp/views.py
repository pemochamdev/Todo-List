from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from todoapp.models import Todo
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.


def home(request):
    get_all_todo = Todo.objects.filter(status = True).order_by('-id')

    if request.method == "POST":
        task = request.POST['task']
        new_task, created = Todo.objects.get_or_create(user=request.user, title=task, status=True)
        new_task.save()
    template_name = 'todoapp/todo.html'
    context = {
        'get_all_todo':get_all_todo,
        #'new_task':new_task,
    }
    return render(request, template_name, context)



def register(request):

    
    if request.method == 'POST':     
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if len(password) <5:
            messages.error(request, 'Password must be at least 5 characters')
            return redirect('register')
        else:
            
            get_all_user_by_username = User.objects.filter(username=username)
             
            if get_all_user_by_username:
                messages.error(request, 'Sorry, This Username Already Exist, Please Try Another One')
                return redirect('register')
            
            new_user = User.objects.create_user(username=username, password=password, email=email)
            new_user.save()
            messages.success(request, "User Successfully Created")
            return redirect('login')

    template_name = 'todoapp/register.html'
    context = {
        #'form':form,
    }
    return render(request, template_name, context)


class CustomLoginView(LoginView):
    template_name = 'todoapp/login.html'
    success_url = 'home'

    def get_success_url(self) -> str:
        return reverse(self.success_url)


class CustomLogoutView(LogoutView):
    success_url = 'index'
    def get_success_url(self) -> str:
        return reverse(self.success_url)

