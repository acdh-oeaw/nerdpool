from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm


from myprodigy.models import Example, NerSample
from myprodigy.utils import nerds_from_ds, nersample_from_answer

NERDPOOL_DEFAULT_NER_SCHEME = getattr(
    settings, 'NERDPOOL_DEFAULT_NER_SCHEME', "NER Labels"
)


class Command(BaseCommand):
    help = 'transforms regular prodigy Example objects to NerSample objects'

    def handle(self, *args, **kwargs):
        to_exclude = list(NerSample.objects.all().values_list('input_hash', flat=True))
        all_samples = Example.objects.all()
        to_process = all_samples.exclude(input_hash__in=to_exclude)
        self.stdout.write(
            self.style.SUCCESS(
                f"Example object count: {all_samples.count()}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"NerSample object count: {NerSample.objects.all().count()}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Example without matching NERSamples: {to_process.count()}"
            )
        )
        for x in tqdm(to_process, total=to_process.count()):
            ds = x.link.first()
            answer = x.ex_as_json()
            ner_dataset = nerds_from_ds(ds)
            try:
                nersample_from_answer(answer, ner_dataset, NERDPOOL_DEFAULT_NER_SCHEME)
            except Exception as e:
                continue
        self.stdout.write(
            self.style.SUCCESS(
                f"NerSample object count: {NerSample.objects.all().count()}"
            )
        )
