import datetime

from django import forms


class MeterForm(forms.Form):
    METER_CHOICES = (
        ("SINGLE_METER", "Single meter"),
        ("MULTIPLE_METERS", "Multiple Meters"),
    )
    from_email = forms.EmailField(required=True)
    client_name = forms.CharField(required=True)
    site_address = forms.CharField(required=True, label="Site Name:")
    mpan_mpr = forms.CharField(required=True, label="MPAN or MPR:")
    meter_serial_number = forms.CharField(required=True, label="Meter Serial Number")
    utility_type = forms.CharField(required=True, label="Utility Type")
    supplier = forms.CharField(required=True, label="Supplier")
    # meter_type = forms.ChoiceField(
    #     choices=METER_CHOICES,
    #     label="Choose Meter Type",
    #     widget=forms.Select(attrs={"id": "meter_type"}),
    # )
    meter_reading = forms.CharField(max_length=100, required=False, label="Meter Reading")


    meter_reading_date = forms.CharField(
        widget=forms.widgets.DateTimeInput(format="%d/%m/%Y"),
        initial=datetime.date.today,
    )
    attachment = forms.FileField(
        required=False, label="Optionally upload a photo of your meter reading"
    )
