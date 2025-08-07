from django import forms
from django.forms import modelform_factory
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from ..models import FarmCalendarActivityType, FarmCalendarActivity, Observation, Alert
from .widgets import ReadOnlyNestedActivitiesWidget


class FarmCalendarActivityTypeSelectionForm(forms.Form):
    activity_type = forms.ModelChoiceField(
        queryset=FarmCalendarActivityType.objects.all(),
        empty_label="Select Activity Type",
        required=True,
        label="Activity Type",
    )


class FarmCalendarActivityTypeForm(forms.ModelForm):
    class Meta:
        model = FarmCalendarActivityType
        fields = ["name", "category","background_color", "border_color", "text_color"]
        widgets = {
            "background_color": forms.TextInput(attrs={"class": "color-picker"}),
            "border_color": forms.TextInput(attrs={"class": "color-picker"}),
            "text_color": forms.TextInput(attrs={"class": "color-picker"}),
        }


class FarmCalendarActivityForm(forms.ModelForm):
    class Meta:
        model = FarmCalendarActivity
        fields = '__all__'
        exclude = [
            'id',
            'parent_activity'
        ]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "activity_type": forms.HiddenInput(),
        }


class ParentActivityForm(FarmCalendarActivityForm):
    nested_activities = forms.ModelMultipleChoiceField(
        queryset=FarmCalendarActivity.objects.none(),
        required=False,
        label="Nested Activities",
        widget=ReadOnlyNestedActivitiesWidget(),
    )
    class Meta(FarmCalendarActivityForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['nested_activities'].queryset = self.instance.nested_activities.all()
            self.initial['nested_activities'] = self.instance.nested_activities.all()


class NestedActivityForm(FarmCalendarActivityForm):
    parent_activity = forms.ModelChoiceField(
        queryset=FarmCalendarActivity.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url='activities-autocomplete', attrs={'class': 'select2'}),
        label="Part of Activity"
    )

    class Meta(FarmCalendarActivityForm.Meta):
        _parent_exc = FarmCalendarActivityForm.Meta.exclude.copy()
        if 'parent_activity' in _parent_exc:
            _parent_exc.remove('parent_activity')
        exclude = _parent_exc

class ObservationForm(NestedActivityForm):
    class Meta(NestedActivityForm.Meta):
        model = Observation
        _parent_exc = NestedActivityForm.Meta.exclude.copy()
        if 'parent_activity' in _parent_exc:
            _parent_exc.remove('parent_activity')
        exclude = _parent_exc + ['responsible_agent', 'agricultural_machinery']


class AlertForm(NestedActivityForm):
    value = forms.CharField(required=False,
                widget=forms.TextInput(attrs={'disabled': 'disabled'}))
    value_unit = forms.CharField(required=False,
                widget=forms.TextInput(attrs={'disabled': 'disabled'}))
    observed_property = forms.CharField(required=False,
                widget=forms.TextInput(attrs={'disabled': 'disabled'}))

    class Meta(NestedActivityForm.Meta):
        model = Alert
        _parent_exc = NestedActivityForm.Meta.exclude.copy()
        _parent_exc.append('responsible_agent')
        _parent_exc.append('agricultural_machinery')
        exclude = _parent_exc

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent_activity'].label = _("Related Observation")
        if self.instance and self.instance.pk and self.instance.parent_activity:
            try:
                parent_observation = self.instance.parent_activity.observation
                if self.instance.parent_activity:
                    self.fields['value'].initial = parent_observation.value
                    self.fields['value_unit'].initial = parent_observation.value_unit
                    self.fields['observed_property'].initial = parent_observation.observed_property
            except Observation.DoesNotExist:
                pass
