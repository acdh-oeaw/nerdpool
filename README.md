# NERDPool

## About

Hardly any resources for the training of NER models for non-contemporary German languages exist. The project NERDPool tries to overcome this issue by preparing a collection of gold standard named entity annotation samples to train (german) time and genre specific NER models.


## prodigy server-start examples

prodigy nerdpool.ner thun de_core_news_sm https://thun-korrespondenz.acdh.oeaw.ac.at::thun::editions --loader from_dsebaseapp --label PER,ORG,LOC -U -F myprodigy/nerdpool_ner.py
