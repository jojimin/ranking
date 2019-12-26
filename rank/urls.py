from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'upload_score', views.upload_score, name='upload_score'),
    url(r'ranking/(?P<client_id>\d+)/(?P<range>\d+-\d+)', views.ranking, name='ranking'),
    url(r'^$', views.index, name='index')
]