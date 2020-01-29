# generated by appcreator
from django.conf.urls import url
from . import views

app_name = 'myprodigy'
urlpatterns = [
    url(
        r'^nerdataset/$',
        views.NerDataSetListView.as_view(),
        name='nerdataset_browse'
    ),
    url(
        r'^nerdataset/detail/(?P<pk>[0-9]+)$',
        views.NerDataSetDetailView.as_view(),
        name='nerdataset_detail'
    ),
    url(
        r'^nerdataset/create/$',
        views.NerDataSetCreate.as_view(),
        name='nerdataset_create'
    ),
    url(
        r'^nerdataset/edit/(?P<pk>[0-9]+)$',
        views.NerDataSetUpdate.as_view(),
        name='nerdataset_edit'
    ),
    url(
        r'^nerdataset/delete/(?P<pk>[0-9]+)$',
        views.NerDataSetDelete.as_view(),
        name='nerdataset_delete'),
    url(
        r'^nersample/$',
        views.NerSampleListView.as_view(),
        name='nersample_browse'
    ),
    url(
        r'^nersample/detail/(?P<pk>[0-9]+)$',
        views.NerSampleDetailView.as_view(),
        name='nersample_detail'
    ),
    url(
        r'^nersample/create/$',
        views.NerSampleCreate.as_view(),
        name='nersample_create'
    ),
    url(
        r'^nersample/edit/(?P<pk>[0-9]+)$',
        views.NerSampleUpdate.as_view(),
        name='nersample_edit'
    ),
    url(
        r'^nersample/delete/(?P<pk>[0-9]+)$',
        views.NerSampleDelete.as_view(),
        name='nersample_delete'),
]
