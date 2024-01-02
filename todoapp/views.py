from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from todoapp.models import Todo

# Create your views here.

@login_required(login_url='login')
def home(request):
    get_all_todo = Todo.objects.filter(user=request.user).order_by('-id') #, status = True

    if request.method == "POST":
        task = request.POST['task']
        new_task, created = Todo.objects.get_or_create(user=request.user, title=task, status=False)
        new_task.save()
    template_name = 'todoapp/todo.html'
    context = {
        'get_all_todo':get_all_todo,
        #'new_task':new_task,
    }
    return render(request, template_name, context)


@login_required(login_url='login')
def delete_task(request, id):
    get_task = get_object_or_404(Todo, id=id, user=request.user)
    get_task.delete()
    return redirect('home')


@login_required(login_url='login')
def update(request, id):
    get_task = get_object_or_404(Todo, id=id, user=request.user)
    get_task.status = True
    get_task.save()
    return redirect('home')
   

def register(request):

    if request.user.is_authenticated:
        return redirect('home')
    
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
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse(self.success_url)

    # def redirect(self, request):
    #     if request.user.is_authenticated:
    #         return redirect('home')
    
   

class CustomLogoutView(LogoutView):
    success_url = 'home'
    def get_success_url(self) -> str:
        return reverse(self.success_url)

