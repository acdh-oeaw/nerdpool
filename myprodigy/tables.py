# generated by appcreator
import django_tables2 as tables
from django_tables2.utils import A
from django.conf import settings

from browsing.browsing_utils import MergeColumn
from .models import (
    NerDataSet,
    NerSample,
    Dataset,
    Example,
    ProdigyServer)


class NerDataSetTable(tables.Table):

    id = tables.LinkColumn(verbose_name='ID')
    ner_name = tables.LinkColumn(verbose_name='Name')
    ner_genre = tables.columns.ManyToManyColumn()

    class Meta:
        model = NerDataSet
        sequence = ('id',)
        attrs = {"class": "table table-responsive table-hover"}
        exclude = ('pw', 'ner_startscript', 'basic_auth_user', 'reverse_proxy')


class NerSampleTable(tables.Table):

    id = tables.LinkColumn(verbose_name='ID')
    text = tables.columns.TemplateColumn("{{ record.as_html|safe}}")
    entities = tables.columns.ManyToManyColumn()
    dataset = tables.columns.ManyToManyColumn()

    class Meta:
        model = NerSample
        sequence = ('id',)
        attrs = {"class": "table table-responsive table-hover"}


class ProdigyServerTable(tables.Table):
    dataset = tables.Column(verbose_name="Dataset", linkify=True)
    link = tables.columns.TemplateColumn(
        f"<a href='{{{{ record.get_external_url }}}}'>{{{{ record.server_hash }}}}"
    )
    status = tables.columns.TemplateColumn("<div id={{ record.server_hash }}></div>")
    up = tables.columns.TemplateColumn(template_name='myprodigy/server_running.html')
    toggle = tables.columns.TemplateColumn(
        template_name='myprodigy/prodigy_toggle_server.html', verbose_name="Toggle server"
    )

    class Meta:
        model = ProdigyServer
