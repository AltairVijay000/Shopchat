from django.urls import path
from . import views


urlpatterns = [
    path('',views.getRoutes),
    path('offers/',views.getOffers),
    path('offers/<str:pk>/',views.getOffer),
]
