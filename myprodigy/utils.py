from vocabs.models import SkosConcept


def get_concepts_from_labels(labels, dataset, scheme):
    label_obj = []
    for x in labels:
        item, _ = SkosConcept.objects.get_or_create(pref_label=f"{x} ({dataset})")
        item.scheme.add(scheme)
        item.save()
        label_obj.append(item)
    return label_obj
