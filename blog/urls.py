from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('detail/<pk>/', views.Detail.as_view(), name="detail"),
    path('create/', views.Create.as_view(), name="create"),
]