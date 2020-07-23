from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

from django.urls import reverse
from django.views import generic
from django.template import loader
from django.conf import settings

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
# Create your views here.


class IndexView(generic.ListView):
	template_name = 'recording/index.html'
	context_object_name = 'recording_list'
	
	def get_queryset(self):
		"""Return the last five published questions."""
		return Voice.objects.all()

class DetailView(generic.DetailView):
	model = Voice
	template_name = 'recording/detail.html'

# Recording new voice
def align_voice(request):
	form = RecordingForm(request.POST, request.FILES)
	# voice_id = form['id']
	# new_rec = form['new_rec'].filename
	
	if form.is_valid():
		rec_id = form.cleaned_data['id']
		# get voice data
		voice = get_object_or_404(Voice, pk=rec_id)
		# get collective dir
		collective_dir = voice.collective.path
		# the onseed of the current seed
		seed_onset = voice.onset
		print("Got filename:", form)
		# get new_recording dir
		root = handle_uploaded_file(request.FILES['new_rec'], rec_id)
		print("root", root)
		print("collective_dir", collective_dir)
		# align new recording and the original collective voice
		align(root, collective_dir, seed_onset)
		# the count of people plus one
		voice.count = voice.count + 1
		# save
		voice.save()
		
		# **********************************************
		# delete root file
		# delete_file(root)
		# **********************************************
		# get new_rec
		# new_rec = AudioSegment.from_file(root, format="wav")
		# play(new_rec)
		# return redirect('/recording/')
		# return redirect('recording: index')
		return JsonResponse({'success':True})
	else:
		return JsonResponse({'error':form.errors})
	'''
	print("Got filename:", fname)
	with contextlib.closing(wave.open(fname,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)
		print(duration)
	'''
	# voice_id = int(request.GET.get('id', None))
	# follow = request.GET.get('new_rec', None)
	# voice = get_object_or_404(Voice, pk=voice_id)

	
	# new_rec = 's'
	# return data
	
	# return HttpResponse("Hello from feedback!")
	
	#return JsonResponse(data)

# handle the new recording
def handle_uploaded_file(f, id):
	root = settings.MEDIA_ROOT + os.sep + str(id) + ".wav"
	delete_file(root)
	# delete_file('C:\\Users\\Aubrey\\Desktop\\semester3\\code\\project-NChant\\nchant\\media\\5.wav')
	with open(root, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return root


# test 
def test(request):
	return render(request, 'recording/test.html')

# test
def new_rec(request):
	return render(request, 'recording/new_rec.html')
# new seed
def new_seed(request):
    return render(request, 'recording/new_seed.html')

def create_seed(request):
	form = VoiceForm(request.POST, request.FILES)
	if form.is_valid():
		voice = form.save(commit=False)
		voice.pub_date = timezone.now()
		# get the id
		try:
			seed_id = Voice.objects.latest('pk').pk + 1
		except:
			seed_id = 1
		root = handle_uploaded_file(request.FILES['seed'], seed_id)
		print("root", root)
		voice.onset = seed_onset(root)
		voice.save()
		return JsonResponse({'success':True})
	else:
		print('error', form.errors)
		return JsonResponse({'error':form.errors})




