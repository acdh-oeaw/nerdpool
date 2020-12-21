import os
import sys
import django
sys.path.append('/app/nerdpool')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nerdpool.settings.server')
django.setup()

from django.conf import settings

from myprodigy.models import NerSample, Dataset, NerDataSet
from myprodigy.utils import nersample_from_answer, nerds_from_ds
from vocabs.models import SkosConceptScheme


NERDPOOL_DEFAULT_NER_SCHEME = getattr(
    settings, 'NERDPOOL_DEFAULT_NER_SCHEME', "NER Labels"
)
<<<end_imports

    def update(answers):
        ner_dataset = nerds_from_ds(dataset)
        scheme, _ = SkosConceptScheme.objects.get_or_create(
            dc_title=NERDPOOL_DEFAULT_NER_SCHEME
        )
        for x in answers:
            nersample_from_answer(x, ner_dataset, scheme)
