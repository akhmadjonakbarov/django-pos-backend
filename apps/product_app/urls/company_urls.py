from django.urls import path
from ..views import company_views

urlpatterns = [
    path('all/', company_views.ListView.as_view()),
    path('add/', company_views.AddView.as_view()),
    path('delete/<int:pk>/', company_views.DeleteView.as_view()),
    path('update/<int:pk>/', company_views.UpdateView.as_view()),
]
