FROM registry.gitlab.com/acdh-oeaw/nlp/prodigy-base-image:1.10.2
LABEL version="0.1"
LABEL description="Docker image to spawn prodigy servers"
COPY . /app
WORKDIR /app
RUN  pip install --upgrade -r requirements.txt && pip install gunicorn psycopg2

RUN mkdir /app/prodigy_recipes
RUN cp /usr/local/lib/python3.8/site-packages/prodigy/recipes/*.py /app/prodigy_recipes
RUN python /app/scripts/patch_prodigy_recipes.py -r /app/prodigy_recipes -t /app/scripts/nerdpool_recipe_patch_template.py -recipes-list ner.py,coref.py,dep.py,image.py,pos.py,rel.py,review.py,terms.py,textcat.py

CMD ["/bin/bash"]
