FROM registry.gitlab.com/acdh-oeaw/nlp/prodigy-base-image:1.10.2
LABEL version="0.1"
LABEL description="Docker image to spawn prodigy servers"
RUN apt-get update -y && apt-get upgrade -y && apt-get install nginx apache2-utils -y
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
RUN pip install -e git+https://github.com/acdh-oeaw/acdh-prodigy-utils.git#egg=prodigy-utils
RUN pip install gunicorn psycopg2
COPY . /app
WORKDIR /app
RUN  pip install --upgrade -r requirements.txt
COPY ./config/default.conf /etc/nginx/conf.d/default.conf
RUN mkdir /app/prodigy_recipes
RUN cp /app/config/prodigy.json /app/prodigy.json
RUN cp /usr/local/lib/python3.8/site-packages/prodigy/recipes/*.py /app/prodigy_recipes
RUN python /app/scripts/patch_prodigy_recipes.py -r /app/prodigy_recipes -t /app/scripts/nerdpool_recipe_patch_template.py -recipes-list ner.py,coref.py,dep.py,image.py,pos.py,rel.py,review.py,terms.py,textcat.py

RUN cp /app/config/nginx.conf /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /app
EXPOSE 81
STOPSIGNAL SIGTERM

CMD ["/app/start.sh"]
