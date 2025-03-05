from django.shortcuts import render,redirect
from .models import User,Task,TaskActivity
from .forms import TaskForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages



def home(request):
    tasks = Task.objects.all()
    context = {"tasks":tasks}
    return render(request,'base/index.html',context)

def add_task(request):
    form = TaskForm()
    context = {"form":form}
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'base/create_task.html',context)

def delete_task(request,pk):
    task = Task.objects.get(id=pk)
    context = {"task":task}
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request,'base/delete_task.html',context)

def edit_task(request,pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    context = {"form":form}
    if request.method == 'POST': 
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'base/create_task.html',context)


#login page
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        try:
            user = User.objects.get(username=username)
        except:
            user = messages.error(request,'User does not exist')
            
        if user:
            login(request,user)
            return redirect('home')
    return render(request,'base/login_register.html')