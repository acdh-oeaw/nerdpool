# Generated by Django 3.0.1 on 2020-01-30 12:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('indentifier', models.URLField(blank=True, default='https://vocabs.acdh.oeaw.ac.at/provide-some-namespace', help_text='URI')),
                ('description', models.TextField(blank=True, help_text='Description of current vocabulary')),
                ('description_lang', models.CharField(blank=True, default='ger', max_length=3, verbose_name='Description language')),
                ('language', models.TextField(blank=True, help_text='If more than one list all using a semicolon ;')),
                ('version', models.CharField(blank=True, help_text='Current version', max_length=300)),
                ('creator', models.TextField(blank=True, help_text='A Person or Organisation responsible for making the vocabulary<br>If more than one list all using a semicolon ;')),
                ('contributor', models.TextField(blank=True, help_text='A Person or Organisation that made contributions to the vocabulary<br>If more than one list all using a semicolon ;')),
                ('subject', models.TextField(blank=True, help_text='The subject of the vocabulary<br>If more than one list all using a semicolon ;')),
                ('owner', models.CharField(blank=True, help_text='A Person or Organisation that own rights for the vocabulary', max_length=300)),
                ('license', models.CharField(blank=True, help_text='A license applied to the vocabulary', max_length=300)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_issued', models.DateField(blank=True, help_text='Date of official resource publication<br>YYYY-MM-DD', null=True)),
                ('relation', models.URLField(blank=True, help_text='e.g. in case of relation to a project, add link to a project website')),
            ],
        ),
        migrations.CreateModel(
            name='SkosCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Collection title or name', max_length=300, verbose_name='skos:prefLabel')),
                ('label_lang', models.CharField(blank=True, default='ger', max_length=3, verbose_name='skos:prefLabel language')),
                ('creator', models.TextField(blank=True, help_text='A Person or Organisation that created a current collection<br>If more than one list all using a semicolon ;', verbose_name='dc:creator')),
                ('legacy_id', models.CharField(blank=True, max_length=200)),
                ('skos_note', models.CharField(blank=True, help_text='Provide some information about a collection', max_length=500, verbose_name='skos:note')),
                ('skos_note_lang', models.CharField(blank=True, default='ger', max_length=3, verbose_name='skos:note language')),
                ('skos_scopenote', models.TextField(blank=True, help_text='Provide detailed description of the collection purpose', verbose_name='skos:scopeNote')),
                ('skos_scopenote_lang', models.CharField(blank=True, default='ger', max_length=3, verbose_name='skos:scopeNote language')),
                ('skos_changenote', models.CharField(blank=True, help_text='Describe significant changes to a collection', max_length=500, verbose_name='skos:changeNote')),
                ('skos_editorialnote', models.CharField(blank=True, help_text='Provide any administrative information, for the purposes of administration and maintenance. E.g. comments on reviewing this collection', max_length=500, verbose_name='skos:editorialNote')),
                ('skos_example', models.CharField(blank=True, max_length=500, verbose_name='skos:example')),
                ('skos_historynote', models.CharField(blank=True, help_text='Describe significant changes to a collection over a time', max_length=500, verbose_name='skos:historyNote')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='SkosLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='The entities label or name.', max_length=100, verbose_name='Label')),
                ('label_type', models.CharField(blank=True, choices=[('prefLabel', 'prefLabel'), ('altLabel', 'altLabel'), ('hiddenLabel', 'hiddenLabel')], help_text='The type of the label.', max_length=30)),
                ('isoCode', models.CharField(blank=True, help_text="The ISO 639-3 code for the label's language.", max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='SkosNamespace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namespace', models.URLField(blank=True, default='https://vocabs.acdh.oeaw.ac.at/provide-some-namespace')),
                ('prefix', models.CharField(blank=True, default='acdh-nerdpool', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SkosConceptScheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dc_title', models.CharField(blank=True, max_length=300, verbose_name='dc:title')),
                ('dc_title_lang', models.CharField(blank=True, default='ger', max_length=3, verbose_name='dc:title language')),
                ('dc_creator', models.TextField(blank=True, help_text='If more than one list all using a semicolon ;', verbose_name='dc:creator')),
                ('dc_description', models.TextField(blank=True, verbose_name='dc:description')),
                ('dc_description_lang', models.CharField(blank=True, default='ger', max_length=3, verbose_name='dc:description language')),
                ('legacy_id', models.CharField(blank=True, max_length=200)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('namespace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vocabs.SkosNamespace')),
            ],
        ),
        migrations.CreateModel(
            name='SkosConcept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pref_label', models.CharField(blank=True, help_text='Preferred label for a concept', max_length=300, verbose_name='skos:prefLabel')),
                ('pref_label_lang', models.CharField(blank=True, default='ger', help_text='Language code of preferred label according to ISO 639-3', max_length=3, verbose_name='skos:prefLabel language')),
                ('definition', models.TextField(blank=True, help_text='Provide a complete explanation of the intended meaning of a concept', verbose_name='skos:definition')),
                ('definition_lang', models.CharField(blank=True, default='ger', max_length=3, verbose_name='skos:definition language')),
                ('notation', models.CharField(blank=True, help_text='A notation is a unique string used        to identify the concept in current vocabulary', max_length=300, verbose_name='skos:notation')),
                ('top_concept', models.BooleanField(default=False, help_text='Is this concept a top concept of main concept scheme?')),
                ('same_as_external', models.TextField(blank=True, help_text='URL of an external Concept with the same meaning<br>If more than one list all using a semicolon ; ', verbose_name='owl:sameAs')),
                ('source_description', models.TextField(blank=True, help_text="A verbose description of the concept's source", verbose_name='Source')),
                ('legacy_id', models.CharField(blank=True, max_length=200)),
                ('name_reverse', models.CharField(blank=True, help_text="Inverse relation like:         'is sub-class of' vs. 'is super-class of'.", max_length=255, verbose_name='name reverse')),
                ('skos_note', models.CharField(blank=True, help_text='Provide some partial information about the meaning of a concept', max_length=500, verbose_name='skos:note')),
                ('skos_note_lang', models.CharField(blank=True, default='ger', max_length=3, verbose_name='skos:note language')),
                ('skos_scopenote', models.TextField(blank=True, help_text='Provide more detailed information of the intended meaning of a concept', verbose_name='skos:scopeNote')),
                ('skos_scopenote_lang', models.CharField(blank=True, default='ger', max_length=3, verbose_name='skos:scopeNote language')),
                ('skos_changenote', models.CharField(blank=True, help_text='Document any changes to a concept', max_length=500, verbose_name='skos:changeNote')),
                ('skos_editorialnote', models.CharField(blank=True, help_text='Provide any administrative information, for the purposes of administration and maintenance. E.g. comments on reviewing this concept', max_length=500, verbose_name='skos:editorialNote')),
                ('skos_example', models.CharField(blank=True, help_text='Provide an example of a concept usage', max_length=500, verbose_name='skos:example')),
                ('skos_historynote', models.CharField(blank=True, help_text='Describe significant changes to the meaning of a concept over a time', max_length=500, verbose_name='skos:historyNote')),
                ('dc_creator', models.TextField(blank=True, help_text='A Person or Organisation that created a current concept<br>If more than one list all using a semicolon ;', verbose_name='dc:creator')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='dct:created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='dct:modified')),
                ('broader_concept', models.ForeignKey(blank=True, help_text='A concept with a broader meaning that a current concept inherits from', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='narrower_concepts', to='vocabs.SkosConcept', verbose_name='Broader Term')),
                ('collection', models.ManyToManyField(blank=True, related_name='has_members', to='vocabs.SkosCollection', verbose_name='member of skos:Collection')),
                ('namespace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vocabs.SkosNamespace')),
                ('other_label', models.ManyToManyField(blank=True, help_text='select other labels that represent this concept', to='vocabs.SkosLabel')),
                ('scheme', models.ManyToManyField(blank=True, related_name='has_concepts', to='vocabs.SkosConceptScheme', verbose_name='skos:ConceptScheme')),
                ('skos_broader', models.ManyToManyField(blank=True, help_text='A concept with a broader meaning', related_name='narrower', to='vocabs.SkosConcept', verbose_name='skos:broader')),
                ('skos_broadmatch', models.ManyToManyField(blank=True, help_text='A concept in an external ConceptSchema with a broader meaning', related_name='narrowmatch', to='vocabs.SkosConcept', verbose_name='skos:broadMatch')),
                ('skos_closematch', models.ManyToManyField(blank=True, help_text='A concept in an external ConceptSchema that has a similar meaning', related_name='closematch', to='vocabs.SkosConcept', verbose_name='skos:closeMatch')),
                ('skos_exactmatch', models.ManyToManyField(blank=True, help_text='A concept in an external ConceptSchema that can be used interchangeably and has an exact same meaning', related_name='exactmatch', to='vocabs.SkosConcept', verbose_name='skos:exactMatch')),
                ('skos_narrower', models.ManyToManyField(blank=True, help_text='A concept with a narrower meaning', related_name='broader', to='vocabs.SkosConcept', verbose_name='skos:narrower')),
                ('skos_narrowmatch', models.ManyToManyField(blank=True, help_text='A concept in an external ConceptSchema with a narrower meaning', related_name='broadmatch', to='vocabs.SkosConcept', verbose_name='skos:narrowMatch')),
                ('skos_related', models.ManyToManyField(blank=True, help_text='An associative relationship among two concepts', related_name='related', to='vocabs.SkosConcept', verbose_name='skos:related')),
                ('skos_relatedmatch', models.ManyToManyField(blank=True, help_text='A concept in an external ConceptSchema that has an associative relationship with a current concept', related_name='relatedmatch', to='vocabs.SkosConcept', verbose_name='skos:relatedMatch')),
            ],
        ),
    ]