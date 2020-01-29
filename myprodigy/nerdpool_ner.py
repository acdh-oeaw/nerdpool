import prodigy
import spacy
import copy

from typing import List, Optional, Union, Iterable, Dict, Any

from prodigy.components.preprocess import split_sentences, add_tokens
from prodigy.components.loaders import get_stream
from prodigy.core import recipe
from prodigy.util import set_hashes, log, split_string, get_labels
from prodigy.util import INPUT_HASH_ATTR, TASK_HASH_ATTR, msg
# configure django
import os
import sys
import django
sys.path.append('/home/csae8092/repos/nerdpool')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nerdpool.settings.pg_local')
django.setup()

from django.conf import settings

from myprodigy.models import NerSample, Dataset
from myprodigy.utils import nersample_from_answer
from vocabs.models import SkosConceptScheme


NERDPOOL_DEFAULT_NER_SCHEME = getattr(
    settings, 'NERDPOOL_DEFAULT_NER_SCHEME', "NER Labels"
)

@recipe(
    "nerdpool.ner",
    # fmt: off
    dataset=(
        "Dataset to save annotations to", "positional", None, str
    ),
    spacy_model=(
        "Loadable spaCy model with an entity recognizer", "positional", None, str
    ),
    source=(
        "Data to annotate (file path or '-' to read from standard input)", "positional", None, str
    ),
    api=(
        "DEPRECATED: API loader to use", "option", "a", str
    ),
    loader=(
        "Loader (guessed from file extension if not set)", "option", "lo", str
    ),
    label=(
        "Comma-separated label(s) to annotate or text file with one label per line",
        "option", "l",
        get_labels
    ),
    exclude=(
        "Comma-separated list of dataset IDs whose annotations to exclude",
        "option", "e",
        split_string
    ),
    unsegmented=(
        "Don't split sentences", "flag", "U", bool
    ),
    # fmt: on
)
def nerdpool_make_gold(
    dataset: str,
    spacy_model: str,
    source: Union[str, Iterable[dict]] = "-",
    api: Optional[str] = None,
    loader: Optional[str] = None,
    label: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    unsegmented: bool = False,
) -> Dict[str, Any]:
    """
    Create gold data for NER by correcting a model's suggestions.
    """
    log("RECIPE: Starting recipe ner.correct (previously ner.make-gold)", locals())
    nlp = spacy.load(spacy_model)
    labels = label  # comma-separated list or path to text file
    if not labels:
        labels = get_labels_from_ner(nlp)
        if not labels:
            msg.fail("No --label argument set and no labels found in model", exits=1)
        msg.text(f"Using {len(labels)} labels from model: {', '.join(labels)}")
    log(f"RECIPE: Annotating with {len(labels)} labels", labels)
    stream = get_stream(source, api, loader, rehash=True, dedup=True, input_key="text")
    if not unsegmented:
        stream = split_sentences(nlp, stream)
    stream = add_tokens(nlp, stream)

    def make_tasks(nlp, stream: Iterable[dict]) -> Iterable[dict]:
        """Add a 'spans' key to each example, with predicted entities."""
        texts = ((eg["text"], eg) for eg in stream)
        for doc, eg in nlp.pipe(texts, as_tuples=True):
            task = copy.deepcopy(eg)
            spans = []
            for ent in doc.ents:
                if labels and ent.label_ not in labels:
                    continue
                spans.append(
                    {
                        "token_start": ent.start,
                        "token_end": ent.end - 1,
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "text": ent.text,
                        "label": ent.label_,
                        "source": spacy_model,
                        "input_hash": eg[INPUT_HASH_ATTR],
                    }
                )
            task["spans"] = spans
            task = set_hashes(task)
            yield task

    stream = make_tasks(nlp, stream)

    def update(answers):
        scheme, _ = SkosConceptScheme.objects.get_or_create(
            dc_title=NERDPOOL_DEFAULT_NER_SCHEME
        )
        cur_dataset = Dataset.objects.get(name=dataset)
        for x in answers:
            nersample_from_answer(x, cur_dataset, scheme)

    return {
        "view_id": "ner_manual",
        "update": update,
        "dataset": dataset,
        "stream": stream,
        "exclude": exclude,
        "config": {"lang": nlp.lang, "labels": labels, "exclude_by": "input"},
    }
