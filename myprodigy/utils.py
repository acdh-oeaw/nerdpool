from vocabs.models import SkosConcept

from . models import Dataset, NerSample


def get_used_labels(sample):
    try:
        labels = set([x.get('label') for x in sample['spans']])
    except KeyError:
        labels = []
    return labels


def get_concepts_from_labels(labels, dataset, scheme):
    label_obj = []
    for x in labels:
        item, _ = SkosConcept.objects.get_or_create(pref_label=f"{x} ({dataset})")
        item.scheme.add(scheme)
        item.save()
        label_obj.append(item)
    return label_obj


def nersample_from_answer(answer, dataset, scheme):
    my_sample, _ = NerSample.objects.get_or_create(
        input_hash=answer['_input_hash'],
        task_hash=answer['_task_hash']
    )
    my_sample.text = answer['text']
    my_sample.orig_example = answer
    my_sample.dataset.add(dataset)
    labels = get_used_labels(answer)
    if labels:
        my_sample.entities.set(get_concepts_from_labels(labels, dataset.name, scheme))
    my_sample.save()
    return my_sample
