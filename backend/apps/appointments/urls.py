"""
Appointments URLs
"""

from django.urls import path
from .views import (
    AvailableSlotsView,
    AppointmentListCreateView,
    AppointmentDetailView,
    AppointmentStatusUpdateView,
    MyAppointmentsView,
    SpecialistScheduleView,
)

urlpatterns = [
    path("slots/", AvailableSlotsView.as_view(), name="available_slots"),
    path("", AppointmentListCreateView.as_view(), name="appointments"),
    path("my/", MyAppointmentsView.as_view(), name="my_appointments"),
    path("<int:pk>/", AppointmentDetailView.as_view(), name="appointment_detail"),
    path("<int:pk>/status/", AppointmentStatusUpdateView.as_view(), name="appointment_status"),
    path("specialist/schedule/", SpecialistScheduleView.as_view(), name="specialist_schedule"),
]
