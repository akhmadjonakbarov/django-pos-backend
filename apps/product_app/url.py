# myapp/item_urls.py

from django.urls import path, include
from .urls import (
    category_urls, company_urls, unit_urls,
    item_urls, document_urls, store_urls,
    doc_item_urls
)

urlpatterns = [
    path('category/', include(category_urls)),
    path('company/', include(company_urls)),
    path('unit/', include(unit_urls)),
    path('item/', include(item_urls)),
    path('document/', include(document_urls)),
    path('store/', include(store_urls)),
    path('doc-item/', include(doc_item_urls)),
]
