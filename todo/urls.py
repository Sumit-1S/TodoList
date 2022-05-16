from django.urls import path,include
from .views import TaskCreate, TaskList, TaskDetail, TaskUpdate, TaskDelete, UserLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns=[
  path('',TaskList.as_view(),name="task"),
  path("task/task-create/",TaskCreate.as_view(),name="task_view"),
  path("task/login/",UserLoginView.as_view(),name="Login"),
  path("Logout/",LogoutView.as_view(next_page="Login"),name="Logout"),
  path("task/register/",RegisterPage.as_view(),name="Register"),
  path('task/<int:pk>/',TaskDetail.as_view(),name='task_detail'),
  path('task/task-update/<int:pk>/',TaskUpdate.as_view(),name='task_update'),
  path('task/task-delete/<int:pk>/', TaskDelete.as_view(), name="task_delete")
]