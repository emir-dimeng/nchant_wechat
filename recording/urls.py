from django.urls import path

from . import views
from . import wechat_views
from django.conf.urls import url

app_name = 'recording'
urlpatterns = [
	# ex: /record/
	path('', views.IndexView.as_view(), name='index'),
	path('test/', views.test, name='test'),

	# ex: /record/5/
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('new_seed', views.new_seed, name='new_seed'),
	path('new_rec', views.new_rec, name='new_rec'),

	url(r'^ajax/align_voice/$', views.align_voice, name='align_voice'),

	url(r'^ajax/create_seed/$', views.create_seed, name='create_seed'),
	# ex: /record/5/results/
	#path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	# ex: /record/5/vote/
	#path('<int:question_id>/vote/', views.vote, name='vote'),
	##
	# Wechat request
	##
	path('wechat_index', wechat_views.wechat_index, name='wechat_index'),
]
