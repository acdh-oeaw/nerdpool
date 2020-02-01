import os
import uuid
from subprocess import Popen

import prodigy
from rest_framework.response import Response
from rest_framework.views import APIView
import asyncio

from myprodigy.models import ProdigyServer

loop = asyncio.get_event_loop()

nginx_templ = """                        
server {{
    listen 81;
    server_name localhost;

    location /static/ {{        
        autoindex on;          
        alias /staticfiles/;   
    }}

    location / {{
        proxy_pass http://nerdpool_prodigy:8000;
        proxy_set_header Host $host;    
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }}
}}

{loc}
"""

nginx_loc = """

server {{
    listen 81;
    server_name {hash}.sisyphos.arz.oeaw.ac.at;
    
    location / {{               
        proxy_pass http://nerdpool_prodigy:{port};
    }}
}}
"""

def start_prodigy_server(prodigy_attrs, new=False):
    if new:
        ports = list(ProdigyServer.objects.all().values_list('port', flat=True).order_by('port'))
        if len(ports) == 0:
            port = 8080
        else:
            port = ports[-1]+1
        uid = uuid.uuid1()
        ProdigyServer.objects.create(port=port, server_hash=uid)
        lc = ""
        for s in ProdigyServer.objects.all():
            lc += nginx_loc.format(hash=s.server_hash, port=s.port)
            print(nginx_templ.format(loc=lc))
        with open('/nginx/default.conf', 'w') as out:
            out.write(nginx_templ.format(loc=lc))
    Popen([f'PRODIGY_PORT={port} prodigy {prodigy_attrs.format(uid=uid)}'], shell=True,
          stdin=None, stdout=None, stderr=None, close_fds=True)
    return uid


class ProdigyServers(APIView):

    def post(self, request):
        prod_attr = "ner.manual {uid} de ./test_data.jsonl --label PERSON,ORG"
        uid = start_prodigy_server(prod_attr, new=True)
        #loop.run_in_executor(None, prodigy.serve("ner.manual ner_news_headlines de ../test_data.jsonl --label PERSON,ORG", port=8081))
        print('went through', uid)
        return Response({'url': f'{uid}.sisyphos.arz.oeaw.ac.at'})