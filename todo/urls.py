from django.urls import path

from . import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('signup', views.SignupView.as_view()),
    path('todo-list', views.TodoListView.as_view()),
    path('todo-list/<int:id>', views.TodoDetailView.as_view())
]