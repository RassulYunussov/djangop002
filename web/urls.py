from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^((?P<id>\d+)/)?$', views.main_page, name='main_page'),
    url(r'^((?P<id>\d+)/)?video/((?P<video>\d+)/)?$', views.videos_page, name='videos_page'),
    # url(r'^new_id/$', views.new_id, name='new_id'),
    url(r'^((?P<id>\d+)/)?start/((?P<video>\d+)/)?$', views.videos_page, {'start': True}, name='videos_page'),
    url(r'^api/cites/$', views.filterCities, name='filter_cities'),
    url(r'^api/vilavi_activity/$', views.vilaviActivity, name='vilavi_activity'),
    url(r'^api/vilavi_qualifications/$', views.vilaviQualification, name='vilavi_qualifications'),
    url(r'^api/vilavi_level/$', views.vilaviLevel, name='vilavi_level'),
    url(r'^api/vilavi_sponsor_id/$', views.vilaviSponsorId, name='vilavi_sponsor_id'),
    url(r'^api/profile_email_exist/$', views.profileEmailExist, name='profile_email_exist'),
    url(r'^api/profile_deactivate/$', views.profileDeactivate, name='profile_deactivate'),
    url(r'^api/profile_info/$', views.profileInfo, name='profile_info'),
    url(r'^api/time_remaining/$', views.timeRemaining, name='time_remaining'),
    url(r'^api/timer_values/$', views.getTimerValues, name='timer_values'),
]
