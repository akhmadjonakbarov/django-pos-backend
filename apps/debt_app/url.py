from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.ListView.as_view(), name='debt-list'),
    path('add/', views.AddView.as_view(), name='add-debt'),
    path('pay/<int:pk>/', views.PayDebtView.as_view(), name='pay-amount'),
    path('update/<int:pk>/', views.UpdateView.as_view(), name='update-debt'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete-debt')
]
