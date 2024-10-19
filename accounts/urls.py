from .views import *
from django.urls import path

urlpatterns = [
    path("login/", login_view, name='login'),  # User login
    path("registration/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path('password_reset/', MyPasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/', MyPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', MyPasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('', profile, name='profile'),
    path('users/', users, name='users'),
    path('users/new/', UsersCreateView.as_view(), name='new_user'),  
    path('users/<int:pk>/', UsersDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/update/', UsersUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UsersDeleteView.as_view(), name='user_delete'),
]