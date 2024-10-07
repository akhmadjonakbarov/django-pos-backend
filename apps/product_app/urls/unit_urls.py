from django.urls import path
from ..views import unit_views

urlpatterns = [
    path('all/', unit_views.ListView.as_view()),
    path('add/', unit_views.AddView.as_view()),
    path('delete/<int:pk>/', unit_views.DeleteView.as_view()),
    path('update/<int:pk>/', unit_views.UpdateView.as_view()),
]
