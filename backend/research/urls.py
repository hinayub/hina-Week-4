from django.urls import path

from .views import ResearchView, ResearchHistoryView

urlpatterns = [
    path("research/", ResearchView.as_view(), name="research"),
    path("research/history/", ResearchHistoryView.as_view(), name="research-history"),
]
