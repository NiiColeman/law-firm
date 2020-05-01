from django import forms
from django.forms import widgets
from .models import Schedule, MeetingSession
# from .widgets import XDSoftDateTimePickerInput, BootstrapDateTimePickerInput, FengyuanChenDatePickerInput

from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


# class TimeInput(forms.TimeInput):
#     input_type = "time"


class ScheduleForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    # start_time = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'], widget=BootstrapDateTimePickerInput())

    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    class Meta:
        model = Schedule
        fields = ("purpose",)


class SessionForm(forms.ModelForm):

    # start_date = forms.DateTimeField(widget=forms.DateTimePickerInput())
    # end_date = forms.DateTimeField(widget=forms.DateTimePickerInput())

    class Meta:
        model = MeetingSession
        fields = ('purpose','room')
        # widgets = {
        #     # default date-format %m/%d/%Y will be used
        #     'start_time': DateTimePickerInput(),
        #     # specify date-frmat
        #     'end_time': DatePickerInput(format='%Y-%m-%d'),
        # }
