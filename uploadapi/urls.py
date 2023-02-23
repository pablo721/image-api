from django.urls import path, include
from .routers import router
from . import views


app_name = 'uploadapi'
urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('images/', include(router.urls)),
    path('links/<int:pk>/', views.links, name='links'),
    path('temp_img/<str:signed_data>', views.temp, name='temp'),
]

