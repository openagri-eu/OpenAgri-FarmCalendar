from rest_framework import permissions, viewsets

from farm_activities.models import (
    FarmCalendarActivity,
    FarmCalendarActivityType,
    Alert,
    FertilizationOperation,
    IrrigationOperation,
    CropProtectionOperation,
    YieldPredictionObservation,
    DiseaseDetectionObservation,
    VigorEstimationObservation,
    SprayingRecommendationObservation,
    Observation,
    CropStressIndicatorObservation,
    CropGrowthStageObservation,
    CompostOperation,
    AddRawMaterialOperation,
    CompostTurningOperation,
)
from ..serializers import (
    FarmCalendarActivitySerializer,
    FarmCalendarActivityTypeSerializer,
    AlertSerializer,
    FertilizationOperationSerializer,
    IrrigationOperationSerializer,
    CropProtectionOperationSerializer,
    YieldPredictionObservationSerializer,
    DiseaseDetectionObservationSerializer,
    VigorEstimationObservationSerializer,
    SprayingRecommendationObservationSerializer,
    ObservationSerializer,
    CropStressIndicatorObservationSerializer,
    CropGrowthStageObservationSerializer,
    CompostOperationSerializer,
    AddRawMaterialOperationSerializer,
    CompostTurningOperationSerializer,
)


class FarmCalendarActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows FarmCalendarActivity to be viewed or edited.
    """
    queryset = FarmCalendarActivity.objects.all().order_by('-start_datetime')
    serializer_class = FarmCalendarActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ['title', 'activity_type', 'responsible_agent']


class FarmCalendarActivityTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows FarmCalendarActivityType to be viewed or edited.
    """
    queryset = FarmCalendarActivityType.objects.all().order_by('-name')
    serializer_class = FarmCalendarActivityTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['name', ]


class AlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Alert to be viewed or edited.
    """
    queryset = Alert.objects.all().order_by('-start_datetime')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title', 'activity_type', 'severity']


class FertilizationOperationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows FertilizationOperation to be viewed or edited.
    """
    queryset = FertilizationOperation.objects.all().order_by('-start_datetime')
    serializer_class = FertilizationOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title', 'activity_type', 'responsible_agent']


class IrrigationOperationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows IrrigationOperation to be viewed or edited.
    """
    queryset = IrrigationOperation.objects.all().order_by('-start_datetime')
    serializer_class = IrrigationOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title', 'activity_type', 'responsible_agent']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('compost_operation_pk'):
            queryset = queryset.filter(parent_activity=self.kwargs['compost_operation_pk'])
        return queryset


class CropProtectionOperationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CropProtectionOperation to be viewed or edited.
    """
    queryset = CropProtectionOperation.objects.all().order_by('-start_datetime')
    serializer_class = CropProtectionOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title', 'activity_type', 'responsible_agent']


class ObservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Observation to be viewed or edited.
    """
    queryset = Observation.objects.all().order_by('-start_datetime')
    serializer_class = ObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title','activity_type']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('compost_operation_pk'):
            queryset = queryset.filter(parent_activity=self.kwargs['compost_operation_pk'])
        return queryset

class CropStressIndicatorObservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CropStressIndicator to be viewed or edited.
    """
    queryset = CropStressIndicatorObservation.objects.all().order_by('-start_datetime')
    serializer_class = CropStressIndicatorObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title','activity_type', 'responsible_agent']


class CropGrowthStageObservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CropGrowthStageObservation to be viewed or edited.
    """
    queryset = CropGrowthStageObservation.objects.all().order_by('-start_datetime')
    serializer_class = CropGrowthStageObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title','activity_type', 'responsible_agent']


class YieldPredictionObservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows YieldPrediction to be viewed or edited.
    """
    queryset = YieldPredictionObservation.objects.all().order_by('-start_datetime')
    serializer_class = YieldPredictionObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title','activity_type', 'parcel']


class DiseaseDetectionObservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows DiseaseDetection to be viewed or edited.
    """
    queryset = DiseaseDetectionObservation.objects.all().order_by('-start_datetime')
    serializer_class = DiseaseDetectionObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title','activity_type', 'parcel']


class VigorEstimationObservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows VigorEstimation to be viewed or edited.
    """
    queryset = VigorEstimationObservation.objects.all().order_by('-start_datetime')
    serializer_class = VigorEstimationObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title','activity_type', 'parcel']


class SprayingRecommendationObservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SprayingRecommendation to be viewed or edited.
    """
    queryset = SprayingRecommendationObservation.objects.all().order_by('-start_datetime')
    serializer_class = SprayingRecommendationObservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title','activity_type', 'parcel']


class CompostOperationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CompostOperation to be viewed or edited.
    """
    queryset = CompostOperation.objects.all().prefetch_related('nested_activities').order_by('-start_datetime')
    serializer_class = CompostOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title','activity_type', 'compost_pile_id']


class AddRawMaterialOperationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AddRawMaterialOperation to be viewed or edited.
    """
    queryset = AddRawMaterialOperation.objects.all().order_by('-start_datetime')
    serializer_class = AddRawMaterialOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title', 'activity_type']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('compost_operation_pk'):
            queryset = queryset.filter(parent_activity=self.kwargs['compost_operation_pk'])
        return queryset

class CompostTurningOperationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CompostTurningOperation to be viewed or edited.
    """
    queryset = CompostTurningOperation.objects.all().order_by('-start_datetime')
    serializer_class = CompostTurningOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['title', 'activity_type']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('compost_operation_pk'):
            queryset = queryset.filter(parent_activity=self.kwargs['compost_operation_pk'])
        return queryset
