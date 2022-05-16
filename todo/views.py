from atexit import register
from dataclasses import fields
from multiprocessing import context
from operator import truediv
from pyexpat import model
from re import template
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django .urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView

class TaskList(LoginRequiredMixin, ListView):
  model = Task
  context_object_name = 'tasks'
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['tasks'] = context['tasks'].filter(user = self.request.user)
      context['count'] = context['tasks'].filter(complete=False).count()
      search_task = self.request.GET.get('search_bar') or ''
      if search_task:
        # context['tasks'] = context['tasks'].filter(title__icontains = search_task)
        context['tasks'] = context['tasks'].filter(title__startswith = search_task)
        context['search_task'] = search_task
      return context


class TaskDetail(LoginRequiredMixin,DetailView):
  model = Task
  context_object_name = 'task'
  template_name = 'todo/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
  model = Task
  fields = ['title','desc','complete']
  # fields = ['title','desc'] #for selected rows
  success_url = reverse_lazy('task')
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
  model = Task
  fields = ['title','desc','complete']
  success_url = reverse_lazy('task')

class TaskDelete(LoginRequiredMixin, DeleteView):
  model = Task
  context_object_name = 'task'
  template_name = 'todo/task_delete.html'
  success_url = reverse_lazy('task')

class UserLoginView(LoginView):
  template_name = 'todo/task_login.html'
  fields = "__all__"
  redirect_authenticated_user=False
  def get_success_url(self) -> str:
      return reverse_lazy('task')

class RegisterPage(FormView):
  template_name = "todo/task_register.html"
  form_class = UserCreationForm
  redirect_unauthenticated_user = True
  success_url = reverse_lazy('task')
  def form_valid(self, form) -> HttpResponse:
    user = form.save()
    if user is not None:
      login(self.request,user)
    return super(RegisterPage,self).form_valid(form)
  
  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('task')
    return super(RegisterPage,self).get(*args,**kwargs)

