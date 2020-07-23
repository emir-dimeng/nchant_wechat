Install:
pip install sounddevice
pip install SoundFile
pip install librosa
pip install numba==0.48 (since librosa needs the old version numba)
pip install pydub
python -m pip install Pillow
-------------------------------------------------------------------------------
Issues:
1. database, the recording_name cannot be the same
2. download button
3. parameters of audio methods
4. No use: librosa.ipynb, align the similar points of two recordings
5. take the 1st onset of the onset group
*6. onset of seed
7. follow the SEED/COLLECTIVE
8. generate requirements.txt
 pip freeze > requirements.txt
9. Environment: nchant-virtualenv
10. MEDIA_ROOT
11. Recording: recorderJs
12. Volum impact
13. Chrome: access Microphone + Sound
	solution: 
	*****
	audio:  {
        sampleRate: 48000,
        channelCount: 2,
        volume: 1.0
    }
	*****
	https://blog.addpipe.com/audio-constraints-getusermedia/

-----------------------------------------------------------------------------------------
Usefull things:

1. cd C:/Users/Aubrey/Desktop/semester3/code

2. The virtual environment is created by using 'python -m venv env', where env is our virtual environment shown by 'ls' command.


3. from django.contrib.postgres.fields import ArrayField
	before that, pip install psycopg2
	
django webdevelopment

1. django-admin startproject prj_name[mysite]

2. cd prj_name

3. python manage.py runserver

4. python manage.py startapp app_name[main]

5. python manage.py migrate
   [run this once you change your project]
   
6. python manage.py makemigrations app_name[main]
	[Let django know that I make a change]

7. python manage.py migrate	
   python manage.py sqlmigrate app_name 0001[app_name/migrations/0001_initial.py]
	[apply the change]
   reference: https://docs.djangoproject.com/en/3.0/intro/tutorial02/
	
8. python manage.py shell
	[python command]
	
9. sqlite3 default
	[access database]

10. How to save files to database in django
	better not to. instead of storing them to sftp /ftp.....
	https://stackoverflow.com/questions/38628770/how-to-save-files-to-database-in-django
	
11. <audio>
	src="{{ voice.voice_record.url }}", not src="{{ voice.voice_record }}"
	https://stackoverflow.com/questions/25101760/playing-audio-through-audio-tag-in-a-django-application/25102081
	
12. Model: FileField
get url (html access)
obj.audio_file.url
get path (server access)
obj.audio_file.path 





--------------------------------------------------------
Django:

create forms from models
https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/

FormData, add CSRF-token
formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

If there are files included in the FormData, then add 'request.FILES' to get form data.
RecordingForm(request.POST, request.FILES)
