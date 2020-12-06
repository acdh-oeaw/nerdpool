from vocabs.models import SkosConcept

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.query import EmptyQuerySet

from . models import NerDataSet, NerSample, Dataset


def limit_access_nersample(qs, user):
    if user.is_superuser:
        pass
    elif user.is_anonymous:
        qs = qs.filter(dataset__is_public=True).distinct()
    else:
        qs = qs.filter(
            Q(
                dataset__is_public=True
            ) |
            Q(
                dataset__ner_annotator=user
            )
        ).distinct()
    return qs


def limit_acces(qs, user):
    if user.is_superuser:
        pass
    elif user.is_anonymous:
        qs = qs.filter(is_public=True).distinct()
    else:
        qs = qs.filter(
            Q(
                ner_annotator=user
            ) |
            Q(
                is_public=True
            )
        ).distinct()
    return qs


def test_access_nersample(object, user):
    rel_datasets = object.dataset.all()
    public_set = rel_datasets.filter(is_public=True)
    if public_set:
        return True
    elif user.is_superuser:
        return True
    else:
        return rel_datasets.filter(ner_annotator=user)


def test_access(object, user):
    if user.is_superuser:
        return True
    elif user.is_anonymous:
        return object.is_public
    else:
        if user in object.ner_annotator.all():
            return True
        else:
            return False


def nerds_from_ds(dataset_name):
    ds = Dataset.objects.get(name=dataset_name)
    ner_dataset, _ = NerDataSet.objects.get_or_create(
        ner_name=ds.name
    )
    if ner_dataset.ner_meta:
        pass
    else:
        ner_dataset.ner_meta = ds.meta.tobytes().decode('utf-8')
    ner_dataset.save()
    return ner_dataset


def get_used_labels(sample):
    try:
        labels = set([x.get('label') for x in sample['spans']])
    except KeyError:
        labels = []
    return labels


def get_concepts_from_labels(labels, dataset, scheme):
    label_obj = []
    for x in labels:
        broader, created = SkosConcept.objects.get_or_create(pref_label=f"{x}")
        if created:
            broader.scheme.add(scheme)
            broader.save()
        else:
            pass
        item, item_created = SkosConcept.objects.get_or_create(pref_label=f"{x} ({dataset})")
        if item_created:
            item.scheme.add(scheme)
            item.broader_concept = broader
            item.save()
        label_obj.append(item)
    return label_obj


def nersample_from_answer(answer, nerdataset, scheme):
    my_sample, _ = NerSample.objects.get_or_create(
        input_hash=answer['_input_hash'],
        task_hash=answer['_task_hash']
    )
    annotator = answer.get('_session_id', None)
    if annotator:
        annotator_str = annotator.split('-')[-1]
        try:
            annotator_user = User.objects.get(username=annotator_str)
            my_sample.annotator = annotator_user
        except ObjectDoesNotExist:
            pass
    my_sample.text = answer['text']
    my_sample.orig_example = answer
    my_sample.answer = f"{answer['answer']}"
    my_sample.dataset.add(nerdataset)
    labels = get_used_labels(answer)
    if labels:
        my_sample.entities.set(get_concepts_from_labels(labels, nerdataset.ner_name, scheme))
    my_sample.save()
    return my_sample
