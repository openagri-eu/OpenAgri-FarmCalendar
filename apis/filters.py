from functools import lru_cache


from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _

from shapely.wkt import loads
from shapely.geometry import Point

from farm_management.models import FarmParcel


@lru_cache(maxsize=10)
def is_point_in_geometry(geometry_wkt, point):
    """Check if point is contained in geometry WKT"""
    if not geometry_wkt:
        return False
    try:
        return loads(geometry_wkt).contains(point)
    except:
        return False


class FarmParcelFilter(filters.FilterSet):
    contains_point = filters.CharFilter(
        label=_("Contains point (lat,lon)"),
        method='filter_contains_point',
        help_text=_("Filter parcels containing this point. Format (EPSG:4326): 'latitude,longitude'")
    )

    class Meta:
        model = FarmParcel
        fields = ['identifier', 'farm', 'parcel_type', 'geo_id', 'status']

    def filter_contains_point(self, queryset, name, value):
        """
        Filter farm parcels that contain the given point.
        Input format: "latitude,longitude" (WGS84 coordinates)
        Both point and parcel geometries are in EPSG:4326.
        """
        try:
            lat, lon  = map(float, value.split(','))
            point = Point(lon, lat)

            query_set_values = queryset.values_list('id', 'geometry')

            matching_ids = [
                parcel_id for parcel_id, geometry in query_set_values
                if is_point_in_geometry(geometry, point)
            ]

            return queryset.filter(id__in=matching_ids)

        except (ValueError, TypeError, AttributeError):
            return queryset.none()
