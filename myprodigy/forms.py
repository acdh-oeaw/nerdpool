# generated by appcreator
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,  Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup

from vocabs.models import SkosConcept
from .api_views import start_prodigy_server
from . models import (
    NerDataSet,
    NerSample,
    Dataset,
    Example
)


class NerDataSetFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(NerDataSetFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'id',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search',
                    'id',
                    'ner_name',
                    'ner_created',
                    'ner_description',
                    'ner_period',
                    'ner_genre',
                    css_id="more"
                    ),
                )
            )


class NerDataSetForm(forms.ModelForm):
    ner_genre = forms.ModelMultipleChoiceField(
        required=False,
        label="genre",
        queryset=SkosConcept.objects.filter(collection__name="ner_genre")
    )
     
    def save(self):
        no = super(NerDataSetForm, self).save()
        if no.prodigyserver_set.all().count() == 0:
            start_prodigy_server(dataset_id=no.pk, new=True)
        return no


    class Meta:
        model = NerDataSet
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(NerDataSetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class NerSampleFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(NerSampleFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    'entities',
                    'dataset',
                    css_id="basic_search_fields"
                ),
                AccordionGroup(
                    'Advanced search',
                    'id',
                    'text',
                    'annotator',
                    css_id="more"
                    ),
                )
            )


class NerSampleForm(forms.ModelForm):
    entities = forms.ModelMultipleChoiceField(
        required=False,
        label="entities",
        queryset=SkosConcept.objects.all()
    )

    class Meta:
        model = NerSample
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(NerSampleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class ProdigyServerFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProdigyServerFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Accordion(
                AccordionGroup(
                    'Basic search options',
                    css_id="basic_search_fields"
                ),
                AccordionGroup(
                    'id',
                    css_id="more"
                ),
            )
        )
