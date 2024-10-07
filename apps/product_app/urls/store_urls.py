from django.urls import path
from ..views import store_views

urlpatterns = [
    path('all/', store_views.GetRemainedItemListView.as_view()),
    path('delete/<int:pk>/', store_views.DeleteItemBalanceView.as_view()),
    path('update/<int:pk>/', store_views.UpdateItemBalanceView.as_view()),
]
