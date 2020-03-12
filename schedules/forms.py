from django import forms
from .models import Schedule
# from .widgets import XDSoftDateTimePickerInput, BootstrapDateTimePickerInput, FengyuanChenDatePickerInput


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


# class TimeInput(forms.TimeInput):
#     input_type = "time"


class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )


# class DateTimeInput(forms.DateTimeInput):
#     input_type = "datetime-local"

#     def __init__(self, **kwargs):
#         kwargs["format"] = "%Y-%m-%dT%H:%M"
#         super().__init__(**kwargs)


class ScheduleForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    # start_time = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'], widget=BootstrapDateTimePickerInput())

    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    class Meta:
        model = Schedule
        fields = ("purpose",)
