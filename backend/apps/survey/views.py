"""
Survey Views
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Count, Q

from .models import SurveyResponse
from .serializers import SurveyResponseSerializer, SurveyCreateSerializer, SurveyStatsSerializer


class SurveyCreateView(generics.CreateAPIView):
    serializer_class = SurveyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class SurveyListView(generics.ListAPIView):
    serializer_class = SurveyResponseSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return SurveyResponse.objects.all()


class MySurveysView(generics.ListAPIView):
    serializer_class = SurveyResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SurveyResponse.objects.filter(customer=self.request.user)


class SurveyStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        surveys = SurveyResponse.objects.all()
        total = surveys.count()

        if total == 0:
            return Response({
                "total_surveys": 0,
                "avg_nps": 0,
                "promoters": 0,
                "passives": 0,
                "detractors": 0,
                "nps_score": 0,
            })

        avg_nps = surveys.aggregate(avg=Avg("nps_score"))["avg"] or 0
        promoters = surveys.filter(nps_score__gte=9).count()
        passives = surveys.filter(nps_score__range=[7, 8]).count()
        detractors = surveys.filter(nps_score__lte=6).count()

        nps_score = ((promoters - detractors) / total) * 100

        return Response({
            "total_surveys": total,
            "avg_nps": round(avg_nps, 2),
            "promoters": promoters,
            "passives": passives,
            "detractors": detractors,
            "nps_score": round(nps_score, 2),
        })


class SpecialistSurveyStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, specialist_id=None):
        pk = specialist_id or request.user.id
        surveys = SurveyResponse.objects.filter(specialist_id=pk)
        total = surveys.count()

        if total == 0:
            return Response({"total_surveys": 0, "avg_nps": 0, "nps_score": 0})

        avg_nps = surveys.aggregate(avg=Avg("nps_score"))["avg"] or 0
        promoters = surveys.filter(nps_score__gte=9).count()
        detractors = surveys.filter(nps_score__lte=6).count()
        nps_score = ((promoters - detractors) / total) * 100

        return Response({
            "total_surveys": total,
            "avg_nps": round(avg_nps, 2),
            "nps_score": round(nps_score, 2),
        })
