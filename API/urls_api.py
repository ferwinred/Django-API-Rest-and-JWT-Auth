from django.urls import path
from .views import RegisterView, LoginView, UsersView, RolesView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UsersView.as_view(), name='users'),
    path('users/<int:id>/', UsersView.as_view(), name='user_by_id'),
    path('roles/', RolesView.as_view(), name='roles'),
    path('roles/<int:id>/', RolesView.as_view(), name='role_by_id')
]