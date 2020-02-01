# generated by appcreator
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import DateRangeField, JSONField

from spacy.displacy import EntityRenderer

from vocabs.models import SkosConcept

from browsing.browsing_utils import model_to_dict


def set_extra(self, **kwargs):
    self.extra = kwargs
    return self


models.Field.set_extra = set_extra


class NerDataSet(models.Model):
    ### NerDataSet(id, ner_name, ner_created, ner_meta, ner_description, ner_period) ###
    ner_name = models.CharField(
        max_length=250,
        verbose_name="ner name",
        help_text="ner_name"
        )
    ner_created = models.IntegerField(
        blank=True, null=True,
        verbose_name="ner created",
        help_text="ner_created"
        )
    ner_meta = JSONField(
        blank=True, null=True,
        verbose_name="ner meta",
        help_text="ner_meta"
        )
    ner_description = models.TextField(
        blank=True, null=True,
        verbose_name="ner description",
        help_text="ner_description"
        )
    ner_period = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="ner period",
        help_text="ner_period"
        )
    ner_genre = models.ManyToManyField(
        SkosConcept,
        related_name='rvn_genre_of_nerdataset',
        blank=True,
        verbose_name="genre",
        help_text="genre"
        )
    ner_annotator = models.ManyToManyField(
        User,
        related_name='rvn_part_of_dataset',
        blank=True,
        verbose_name="Annotators",
        help_text="Annotators working on this project"
        )
    ner_startscript = models.TextField(
        blank=True,
        null=True,
        verbose_name="start a server",
        help_text="Command prompt to start a prodigy server"
    )

    class Meta:

        ordering = [
            'id',
        ]
        verbose_name = "ner data set"

    def __str__(self):
        return "{}".format(self.ner_name)

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse('myprodigy:nerdataset_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('myprodigy:nerdataset_create')

    def get_absolute_url(self):
        return reverse('myprodigy:nerdataset_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('myprodigy:nerdataset_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('myprodigy:nerdataset_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('myprodigy:nerdataset_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'myprodigy:nerdataset_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'myprodigy:nerdataset_detail',
                kwargs={'pk': prev.first().id}
            )
        return False


class NerSample(models.Model):
    ### NerSample(id, input_hash, task_hash, text, orig_example) ###
    input_hash = models.BigIntegerField(
        blank=True, null=True,
        verbose_name="input hash",
        help_text="input_hash"
        )
    task_hash = models.BigIntegerField(
        blank=True, null=True,
        verbose_name="task hash",
        help_text="task_hash"
        )
    text = models.TextField(
        blank=True, null=True,
        verbose_name="text",
        help_text="text"
        )
    answer = models.CharField(
        blank=True, null=True,
        max_length=50,
        default="accept",
        verbose_name="answer",
        help_text="answer"
        )
    orig_example = JSONField(
        blank=True, null=True,
        verbose_name="orig example",
        help_text="orig_example"
        )
    entities = models.ManyToManyField(
        SkosConcept,
        related_name='rvn_mentioned_in_nersample',
        blank=True,
        verbose_name="entities",
        help_text="entities"
        )
    dataset = models.ManyToManyField(
        "NerDataSet",
        related_name='rvn_has_nersample',
        blank=True,
        verbose_name="dataset",
        help_text="dataset"
        )
    annotator = models.ForeignKey(
        User,
        models.SET_NULL,
        related_name='rvn_annotates',
        blank=True,
        null=True,
        verbose_name="annotator",
        help_text="Creator of the Annotation"
    )

    class Meta:

        ordering = [
            'id',
        ]
        verbose_name = "ner sample"

    def __str__(self):
        ents = " ".join([x.pref_label for x in self.entities.all()])
        return f"Text: {self.text[:25]}...; Entities: ({ents})"

    def field_dict(self):
        return model_to_dict(self)

    def get_spans(self):
        return self.orig_example['spans']

    def as_html(self):
        return EntityRenderer().render_ents(self.text, self.get_spans(), None)

    @classmethod
    def get_listview_url(self):
        return reverse('myprodigy:nersample_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('myprodigy:nersample_create')

    def get_absolute_url(self):
        return reverse('myprodigy:nersample_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('myprodigy:nersample_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('myprodigy:nersample_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('myprodigy:nersample_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'myprodigy:nersample_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'myprodigy:nersample_detail',
                kwargs={'pk': prev.first().id}
            )
        return False


class Dataset(models.Model):
    name = models.CharField(unique=True, max_length=250)
    created = models.IntegerField()
    meta = models.BinaryField()
    session = models.BooleanField()

    class Meta:
        db_table = 'dataset'

    def __str__(self):
        return f"{self.name}"


class Example(models.Model):
    input_hash = models.BigIntegerField()
    task_hash = models.BigIntegerField()
    content = models.BinaryField()
    link = models.ManyToManyField(
        Dataset, db_table='link',
        related_name='rvn_has_example',
    )

    class Meta:
        db_table = 'example'

    def ex_as_json(self):
        return json.loads(self.content.tobytes().decode('utf-8'))

    def __str__(self):
        mytext = self.ex_as_json().get('text')
        return mytext


class ProdigyServer(models.Model):
    server_hash = models.CharField(unique=True, max_length=250)
    port = models.IntegerField()
    users = models.ManyToManyField(to=User)
