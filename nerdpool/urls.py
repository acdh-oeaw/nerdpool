from django.conf.urls import url, include, handler404
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from vocabs import api_views

from myprodigy import api_views as nerdpool_api_views

# from myprodigy.api_views import NerSampleList

router = routers.DefaultRouter()
router.register(r'skoslabels', api_views.SkosLabelViewSet)
router.register(r'skosnamespaces', api_views.SkosNamespaceViewSet)
router.register(r'skosconceptschemes', api_views.SkosConceptSchemeViewSet)
router.register(r'skosconcepts', api_views.SkosConceptViewSet)
router.register(r'nersapmles', nerdpool_api_views.NerSampleViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^netvis/', include('netvis.urls', namespace="netvis")),
    url(r'^vocabs/', include('vocabs.urls', namespace="vocabs")),
    url(r'^vocabs-ac/', include('vocabs.dal_urls', namespace='vocabs-ac')),
    url(r'^browsing/', include('browsing.urls', namespace='browsing')),
    url(r'^myprodigy/', include('myprodigy.urls', namespace='myprodigy')),
    url(r'^info/', include('infos.urls', namespace='info')),
    url(r'^', include('webpage.urls', namespace='webpage')),
]

handler404 = 'webpage.views.handler404'
