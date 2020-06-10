from django.urls import path
from .views import AutoListView, AutoDetailView, StatisticsView

app_name = "api"

urlpatterns = [
    path('', AutoListView.as_view()),
    path('statistics/', StatisticsView.as_view()),
    path('<slug:slug>/', AutoDetailView.as_view()),
]