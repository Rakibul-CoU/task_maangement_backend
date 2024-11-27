from django.urls import path

from api.views import HomeView, LoginView, RegisterView, TaskAddView, TaskEditView, TaskListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('task-list/', TaskListView.as_view() , name='task-list'),
    path('task-edit/<int:task_id>/', TaskEditView.as_view(), name='task-edit'),
    path('task-create/', TaskAddView.as_view(), name='task-create'),
]