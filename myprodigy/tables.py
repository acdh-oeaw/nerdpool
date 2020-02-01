# generated by appcreator
import django_tables2 as tables
from django_tables2.utils import A

from browsing.browsing_utils import MergeColumn
from . models import (
    NerDataSet,
    NerSample,
    Dataset,
    Example
)


class NerDataSetTable(tables.Table):

    id = tables.LinkColumn(verbose_name='ID')
    ner_name = tables.LinkColumn(verbose_name='Name')
    ner_genre = tables.columns.ManyToManyColumn()

    class Meta:
        model = NerDataSet
        sequence = ('id',)
        attrs = {"class": "table table-responsive table-hover"}


class NerSampleTable(tables.Table):

    id = tables.LinkColumn(verbose_name='ID')
    text = tables.columns.TemplateColumn("{{ record.as_html|safe}}")
    entities = tables.columns.ManyToManyColumn()
    dataset = tables.columns.ManyToManyColumn()

    class Meta:
        model = NerSample
        sequence = ('id',)
        attrs = {"class": "table table-responsive table-hover"}
