from django import forms
from django.conf import settings

class RecordingForm(forms.Form):
	# source recording id
	id = forms.IntegerField()
	# new recording
	new_rec = forms.FileField()
