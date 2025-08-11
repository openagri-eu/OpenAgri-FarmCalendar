import uuid
import datetime
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator



class FarmCalendarActivityType(models.Model):
    """
    This refers to a generic types of activity that is displayed on the farm calendar.
    It is used to represent both observation types and operation types,
    with a descrition of what is this type of activity, and the colors that should be used
    to represent this in the calendar.
    The list of default farm activity types is set on settings.DEFAULT_CALENDAR_ACTIVITY_TYPES.
    These default types are main activity types (observations and operations) already identified
    during development. However, the user may add their own generic activity type that is not
    covered by the defaults.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False, unique=True,
                          blank=False, null=False, verbose_name='ID')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    # Fields for color codes
    background_color = models.CharField(
        max_length=7,
        validators=[RegexValidator(regex='^#[0-9A-Fa-f]{6}$', message='Enter a valid hex color code.')],
        default='#007bff',  # Default color
    )
    border_color = models.CharField(
        max_length=7,
        validators=[RegexValidator(regex='^#[0-9A-Fa-f]{6}$', message='Enter a valid hex color code.')],
        default='#007bff',  # Default color
    )
    text_color = models.CharField(
        max_length=7,
        validators=[RegexValidator(regex='^#[0-9A-Fa-f]{6}$', message='Enter a valid hex color code.')],
        default='#000000',  # Default text color
    )

    class ActivityCategoryChoices(models.TextChoices):
        ACTIVITY = 'activity', _('Activity')
        OBSERVATION = 'observation', _('Observation')
        ALERT = 'alert', _('Alert')

    category = models.CharField(max_length=50, choices=ActivityCategoryChoices.choices,
                                        default=ActivityCategoryChoices.ACTIVITY)


    def __str__(self):
        return self.name


class FarmCalendarActivity(models.Model):
    """
    An occurrence of some farm activity on the calendar.
    This will be the base for both the operations and observations, as in
    how they are presented in a calendar and what type of activity (or event) this is about.
    """
    class Meta:
        verbose_name = "Farm Activity"
        verbose_name_plural = "Farm Activities"

    ACTIVITY_NAME = None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False, unique=True,
                          blank=False, null=False, verbose_name='ID')

    activity_type = models.ForeignKey(FarmCalendarActivityType, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    start_datetime = models.DateTimeField(default=datetime.datetime.now)
    end_datetime = models.DateTimeField(blank=True, null=True)

    details = models.TextField(blank=True, null=True)

    responsible_agent = models.CharField(blank=True, null=True)
    # need to change this into a operation model instead...
    agricultural_machinery = models.ManyToManyField('farm_management.AgriculturalMachine', related_name='used_in_operations', blank=True)
    # weather_observation = models.ManyToManyField('farm_management.AgriculturalMachine', related_name='used_in_operations', blank=True, null=True)?



    parent_activity = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="nested_activities",  # This will act as the reverse relation
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.start_datetime.strftime('%Y-%m-%d %H:%M')})"

    def save(self, *args, **kwargs):
        if self.activity_type is None and self.ACTIVITY_NAME is not None:
            self.activity_type, _ = FarmCalendarActivityType.objects.get_or_create(name=self.ACTIVITY_NAME)

        if self.title is None or self.title == '':
            self.title = self.activity_type.name

        super().save(*args, **kwargs)


class Observation(FarmCalendarActivity):
    sensor_id = models.CharField(_('Made By Sensor'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Observation"
        verbose_name_plural = "Observations"

    value = models.CharField(max_length=255)
    value_unit = models.CharField(max_length=255, blank=True, null=True)
    observed_property = models.CharField(max_length=255)


class Alert(FarmCalendarActivity):
    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"


    class AlertSeverityChoices(models.TextChoices):
        MINOR = 'minor', _('Minor')
        MODERATE = 'moderate', _('Moderate')
        SEVERE = 'severe', _('Severe')
        MAJOR = 'major', _('Major')
        CRITICAL = 'critical', _('Critical')


    severity = models.CharField(_('Severity'), max_length=255, choices=AlertSeverityChoices.choices, default=AlertSeverityChoices.MODERATE)


class BaseParcelAreaObservation(Observation):
    parcel = models.ForeignKey('farm_management.FarmParcel', on_delete=models.CASCADE, verbose_name=_('Has Parcel'))
    area = models.DecimalField(_('Has Area'), max_digits=15, decimal_places=2, default=0.0)

    class Meta:
        abstract = True
        verbose_name = "Base Parcel Area Observation"
        verbose_name_plural = "Base Parcel Area Observations"
