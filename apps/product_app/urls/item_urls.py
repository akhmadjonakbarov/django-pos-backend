from django.urls import path
from ..views import item_views

urlpatterns = [
    path('all/', item_views.ItemListView.as_view()),
    path('add/', item_views.ItemAddView.as_view()),
    path('delete/<int:pk>/', item_views.ItemDeleteView.as_view()),
    path('update/<int:pk>/', item_views.ItemUpdateView.as_view()),
]
