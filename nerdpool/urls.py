from django.conf.urls import url, include, handler404
from django.contrib import admin
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^netvis/', include('netvis.urls', namespace="netvis")),
    url(r'^vocabs/', include('vocabs.urls', namespace="vocabs")),
    url(r'^browsing/', include('browsing.urls', namespace='browsing')),
    url(r'^myprodigy/', include('myprodigy.urls', namespace='myprodigy')),
    url(r'^info/', include('infos.urls', namespace='info')),
    url(r'^', include('webpage.urls', namespace='webpage')),
]

handler404 = 'webpage.views.handler404'
