# generated by appcreator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from . filters import *
from . forms import *
from . tables import *
from . utils import limit_acces, test_access, limit_access_nersample, test_access_nersample
from .models import (
    NerDataSet,
    NerSample,
    ProdigyServer
)
from browsing.browsing_utils import (
    GenericListView, BaseCreateView, BaseUpdateView, BaseDetailView
)


class NerDataSetListView(GenericListView):

    model = NerDataSet
    filter_class = NerDataSetListFilter
    formhelper_class = NerDataSetFilterFormHelper
    table_class = NerDataSetTable
    init_columns = [
        'id', 'ner_name'
    ]
    enable_merge = False

    def get_queryset(self, **kwargs):
        user = self.request.user
        qs = super(NerDataSetListView, self).get_queryset()
        qs = limit_acces(qs, user)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs


class UserDetailView(BaseDetailView):

    model = User
    template_name = 'myprodigy/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        ds = NerDataSet.objects.filter(ner_annotator=obj)
        samples = NerSample.objects.filter(annotator=obj)
        all_samples = NerSample.objects.all().count()
        servers = ProdigyServer.objects.filter(dataset__in=ds)
        context['datasets'] = ds
        context['samples'] = samples
        context['all_samples'] = all_samples
        context['servers'] = servers
        return context


class NerDataSetDetailView(UserPassesTestMixin, BaseDetailView):

    model = NerDataSet
    template_name = 'myprodigy/nerdataset_detail.html'

    def test_func(self):
        user = self.request.user
        cur_obj = self.get_object()
        grant_access = test_access(cur_obj, user)
        return grant_access


class NerDataSetCreate(BaseCreateView):

    model = NerDataSet
    form_class = NerDataSetForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NerDataSetCreate, self).dispatch(*args, **kwargs)


class NerDataSetUpdate(BaseUpdateView):

    model = NerDataSet
    form_class = NerDataSetForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NerDataSetUpdate, self).dispatch(*args, **kwargs)


class NerDataSetDelete(DeleteView):
    model = NerDataSet
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('myprodigy:nerdataset_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NerDataSetDelete, self).dispatch(*args, **kwargs)


class NerSampleListView(GenericListView):

    model = NerSample
    filter_class = NerSampleListFilter
    formhelper_class = NerSampleFilterFormHelper
    table_class = NerSampleTable
    init_columns = [
        'id', 'text',
    ]
    enable_merge = False

    def get_queryset(self, **kwargs):
        user = self.request.user
        qs = super(NerSampleListView, self).get_queryset()
        qs = limit_access_nersample(qs, user)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs


class NerSampleDetailView(UserPassesTestMixin, BaseDetailView):

    model = NerSample
    template_name = 'myprodigy/nersample_detail.html'

    def test_func(self):
        user = self.request.user
        cur_obj = self.get_object()
        grant_access = test_access_nersample(cur_obj, user)
        return grant_access


class NerSampleCreate(BaseCreateView):

    model = NerSample
    form_class = NerSampleForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NerSampleCreate, self).dispatch(*args, **kwargs)


class NerSampleUpdate(BaseUpdateView):

    model = NerSample
    form_class = NerSampleForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NerSampleUpdate, self).dispatch(*args, **kwargs)


class NerSampleDelete(DeleteView):
    model = NerSample
    template_name = 'webpage/confirm_delete.html'
    success_url = reverse_lazy('myprodigy:nersample_browse')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NerSampleDelete, self).dispatch(*args, **kwargs)


class ServerListView(GenericListView):

    model = ProdigyServer
    filter_class = ProdigyServerListFilter
    formhelper_class = ProdigyServerFilterFormHelper
    table_class = ProdigyServerTable
    init_columns = [
        'dataset',
        'link',
        'status',
        'up',
        'toggle'
    ]
    enable_merge = False

    def get_queryset(self, **kwargs):
        qs = super(ServerListView, self).get_queryset(**kwargs)
        if self.request.user.is_superuser:
            return qs
        elif self.request.user.is_authenticated:
            return qs.filter(dataset__ner_annotator=self.request.user)
        else:
            return HttpResponseForbidden()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ServerListView, self).dispatch(*args, **kwargs)
