from django.urls import path
from ..views import document_view as views

urlpatterns = [
    path('all/', views.ListView.as_view()),
    path('sold/', views.SoldItemListView.as_view()),
    path('buy/', views.CreateBuyDocument.as_view()),
    path('sell/', views.CreateSellDocument.as_view()),
    path('delete/<int:pk>/', views.DeleteView.as_view())
]
