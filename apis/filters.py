from django_filters import rest_framework as filters
from django.contrib.gis.geos import Point, GEOSGeometry
from django.db.models import F, Func, Value
from django.db.models.functions import Cast
from django.contrib.gis.db.models.fields import GeometryField
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from farm_management.models import FarmParcel

class FarmParcelFilter(filters.FilterSet):
    # Existing field filters will be automatically included
    contains_point = filters.CharFilter(label=_("Contain's point"), method='filter_contains_point')

    class Meta:
        model = FarmParcel
        fields = ['identifier', 'farm', 'parcel_type', 'geo_id', 'status']

    # This is the key - it ensures proper form rendering
    # @property
    # def qs(self):
    #     queryset = super().qs
    #     return queryset


    def filter_contains_point(self, queryset, name, value):
        """
        Filter farm parcels that contain the given point in their polygon.
        Expected input format: "latitude,longitude" or "latitude,longitude,tolerance"
        """
        import ipdb; ipdb.set_trace()
        try:
            parts = value.split(',')
            if len(parts) == 2:
                lat, lon = map(float, parts)
                tolerance = 0.0
            elif len(parts) == 3:
                lat, lon, tolerance = map(float, parts)
            else:
                return queryset.none()

            point = Point(lon, lat, srid=4326)

            # Convert WKT text field to geometry for comparison
            queryset = queryset.annotate(
                geom=Func(
                    F('geometry'),
                    function='ST_GeomFromText',
                    output_field=GeometryField()
                )
            )

            if tolerance > 0:
                # Create buffer and check intersection
                return queryset.filter(
                    geom__intersects=point.buffer(tolerance)
                )
            else:
                # Exact containment check
                return queryset.filter(geom__contains=point)

        except (ValueError, TypeError):
            return queryset.none()
