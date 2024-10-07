from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.ListView.as_view()),
    path('add/', views.AddView.as_view()),
    path('delete/<int:pk>/', views.DeleteView.as_view()),
    path('update/<int:pk>/', views.UpdateView.as_view()),
]
