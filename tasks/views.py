from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView, FormView
from django.urls import reverse_lazy
from . models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Used built in class based views for this project

#Custom login class view that inherits from django login View
class CustomLoginView(LoginView):
    #Our login template
    template_name = 'tasks/login.html'
    #Use all fields
    fields = '__all__'

    #When user is authenticated they will be redirected
    redirect_authenticated_user = True

    #When user is authenticated redirect them to the tasks url
    def get_success_url(self):
        return reverse_lazy('tasks')

#Register login class view that inherits from from django form view
class Register(FormView):
    template_name = 'tasks/register.html '
    #Form that creates a user that uses django user creation form
    form_class = UserCreationForm
    #redirect authenticated user
    redirect_authenticated_user = True
    #redirect user to tasks url
    success_url = reverse_lazy('tasks')

    #function to login user after registering
    def form_valid(self,form):
        #save the new user
        user = form.save()
        #If user is created login
        if user is not None:
            login(self.request, user)
        return super(Register,self).form_valid(form)

    #function to redirect authenticated user from the register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register, self).get(*args, **kwargs)
    
#A display ListView that represents a list of objects with mixin to restrict and redirect unloged in user
class Tasks(LoginRequiredMixin,ListView):
    model = Task
    #customise queryset name to tasks
    context_object_name = 'tasks'
    #Customise template name to tasks
    template_name = 'tasks/home.html'

    #function to ensure a user only sees their data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Filter the tasks to only be that of the user
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        #Search a user sends, it can also be empty
        search_input =self.request.GET.get('search-area') or ''

        #If the user enters the search item return only thr tasks that start with what the user inputs
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        context['search_input'] = search_input

        #return context data
        return context

#task detail view class that inherits from django detail view class with mixin to restrict and redirect unloged in user
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    #customise quiryset name to tasks
    context_object_name = 'task'
    #Customise template name to tasks
    template_name = 'tasks/task.html'

# Create task class view that inherits from django Create View class with mixin to restrict and redirect unloged in user
class CreateTask(LoginRequiredMixin,CreateView):
    model = Task
    #Specify the fields that we want for the form
    fields = ['title', 'description', 'complete']
    #when the form is submited redirect user to tasks url
    success_url = reverse_lazy('tasks')

    #Method to to add task to logged in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)

#Create Update Task class view that inherits from django Update view class with mixin to restrict and redirect unloged in user
#class is simmilar to Create task class
class UpdateTask(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

#delete task class view that inherits from django Delete view class with mixin to restrict and redirect unloged in user
class DeleteTask(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')