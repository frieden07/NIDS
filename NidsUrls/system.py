from django.urls import path
from NidsViews.system import (
    ChartView,
    IntrusionView,
    AlertView,
    AllAlertView,
    AllIntrusionView,
)

urlpatterns = [
    path("chart", ChartView.as_view()),
    path("allIntrusion", AllIntrusionView.as_view()),
    path("intrusion", IntrusionView.as_view()),
    path("allAlert", AllAlertView.as_view()),
    path("alert", AlertView.as_view()),
]
