from django.urls import path
from .views import StatisticsView

urlpatterns = [
    path('all/', StatisticsView.as_view(), name='statistics'),
]
