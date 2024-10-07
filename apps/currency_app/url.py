from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.ListView.as_view(), name='currency-list'),
    path('add/', views.AddView.as_view(), name='add-currency'),
    path('update/<int:pk>/', views.UpdateView.as_view(), name='update-currency'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete-currency'),
]
