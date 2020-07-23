from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from django.urls import reverse
from django.views import generic
from django.template import loader
from django.conf import settings
from django.db import models

from .models import Voice, VoiceForm
from .forms import RecordingForm
from .alignment import align, delete_file, seed_onset

from pydub import AudioSegment
from pydub.playback import play
from django.forms import modelformset_factory

import os
from django.utils import timezone

import cgitb
import cgi
import contextlib
cgitb.enable()
# 
# views of wechat

JSONSerializer = serializers.get_serializer("json")

class JSONWithURLSerializer(JSONSerializer):

    def handle_field(self, obj, field):
        value = field.value_from_object(obj)
        print('value', value)
        if isinstance(field, models.FileField) | isinstance(field, models.ImageField):
            self._current[field.name] = value.url
        else:
            return super(JSONWithURLSerializer, self).handle_field(obj, field)




# index page
def wechat_index(request):
	nchant_list = Voice.objects.order_by('count')
	#nchant_list = serializers.serialize("json", nchant_list, ensure_ascii=False)
	serializer = JSONWithURLSerializer()
	serializer.serialize(nchant_list)
	nchant_list = serializer.getvalue()
	print(nchant_list)
	# return JsonResponse(context)
	return HttpResponse(nchant_list, content_type="application/json")
