import json
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField

from browsing.browsing_utils import model_to_dict
from vocabs.models import SkosConcept


class Dataset(models.Model):
    name = models.CharField(unique=True, max_length=250)
    created = models.IntegerField()
    meta = models.BinaryField()
    session = models.BooleanField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dataset'

    def __str__(self):
        return f"{self.name}"

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse('myprodigy:dataset_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('myprodigy:dataset_create')

    def get_absolute_url(self):
        return reverse('myprodigy:dataset_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('myprodigy:dataset_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('myprodigy:dataset_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('myprodigy:dataset_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'myprodigy:dataset_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'myprodigy:dataset_detail',
                kwargs={'pk': prev.first().id}
            )
        return False


class NerSample(models.Model):
    input_hash = models.BigIntegerField(null=True, blank=True)
    task_hash = models.BigIntegerField(null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    entities = models.ManyToManyField(
        SkosConcept,
        blank=True,
        related_name='rvn_mentioned_in_nersample',
    )
    dataset = models.ManyToManyField(
        Dataset,
        blank=True,
        related_name='rvn_has_nersample',
    )
    orig_example = JSONField(blank=True, null=True)


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

    def field_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_listview_url(self):
        return reverse('myprodigy:example_browse')

    @classmethod
    def get_createview_url(self):
        return reverse('myprodigy:example_create')

    def get_absolute_url(self):
        return reverse('myprodigy:example_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('myprodigy:example_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('myprodigy:example_delete', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('myprodigy:example_edit', kwargs={'pk': self.id})

    def get_next(self):
        next = self.__class__.objects.filter(id__gt=self.id)
        if next:
            return reverse(
                'myprodigy:example_detail',
                kwargs={'pk': next.first().id}
            )
        return False

    def get_prev(self):
        prev = self.__class__.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return reverse(
                'myprodigy:example_detail',
                kwargs={'pk': prev.first().id}
            )
        return False
