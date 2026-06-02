"""
Survey URLs
"""

from django.urls import path
from .views import (
    SurveyCreateView, SurveyListView,
    MySurveysView, SurveyStatsView,
    SpecialistSurveyStatsView,
)

urlpatterns = [
    path("submit/", SurveyCreateView.as_view(), name="survey_submit"),
    path("list/", SurveyListView.as_view(), name="survey_list"),
    path("my/", MySurveysView.as_view(), name="my_surveys"),
    path("stats/", SurveyStatsView.as_view(), name="survey_stats"),
    path("stats/<int:specialist_id>/", SpecialistSurveyStatsView.as_view(), name="specialist_survey_stats"),
]
