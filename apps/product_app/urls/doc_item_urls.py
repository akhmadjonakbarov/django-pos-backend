from django.urls import path
from ..views import doc_item_views

urlpatterns = [
    path('all/', doc_item_views.ListView.as_view()),
    path('all/buy/', doc_item_views.BuyListView.as_view()),
    path('by-doc-id/<int:doc_id>/', doc_item_views.ItemByDocumentIdListView.as_view()),
    path('delete/<int:pk>/', doc_item_views.DeleteView.as_view()),
]
