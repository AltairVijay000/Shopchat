from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('offer/<str:pk>/', views.offer, name="offer"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-offer/', views.createOffer, name="create-offer"),
    path('update-offer/<str:pk>/', views.updateOffer, name="update-offer"),
    path('delete-offer/<str:pk>/', views.deleteOffer, name="delete-offer"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]
