from django.db import models
from django.forms import ModelForm

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import NON_FIELD_ERRORS

# Create your models here.
class Voice(models.Model):

	# Title
	title = models.CharField(max_length=100, default='none')
	# Initiator
	initiator = models.CharField(max_length=100, default='none')
	# uplodate date
	pub_date = models.DateTimeField('date published', default=timezone.now())
	# Description
	description = models.CharField(max_length=300, default='none')
	# image
	image = models.ImageField(upload_to=settings.MEDIA_ROOT, height_field=None, width_field=None, 
		default=settings.MEDIA_ROOT+'default.jpg')
	# collective
	collective = models.FileField(upload_to=settings.MEDIA_ROOT, default='none')
	# seed
	seed = models.FileField(upload_to=settings.MEDIA_ROOT, default='none')
	# count 
	count = models.IntegerField(default=0)
	# onset
	onset = models.FloatField(default=0.0)

	# pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.title

# Form class
class VoiceForm(ModelForm):
	class Meta:
		model = Voice
		# fields = '__all__'
		fields = ['title', 'initiator', 'description', 
				  'image', 'collective', 'seed', 'count']
		error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
