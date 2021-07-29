from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('update_profile/<int:pk>/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('new_account/', views.CreateNewUser.as_view(), name="new_account")
]