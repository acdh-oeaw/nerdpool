import os
import signal
import uuid
from subprocess import Popen
import psutil
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from myprodigy.models import ProdigyServer, NerDataSet


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
    server_name {hash}.{prodigy_base_url};

    location / {{
        satisfy any;

        allow 10.4.24.0/24;
        allow 127.0.0.1;
        deny all;

        auth_basic "Provide a password";
        auth_basic_user_file /etc/nginx/conf.d/.passwd;
        proxy_pass http://nerdpool_prodigy:{port};
    }}
}}
"""

PRODIGY_BASE_URL = getattr(settings, "PRODIGY_BASE_URL", "pd.sisyphos.arz.oeaw.ac.at")


def create_prodigy_command(ds):
    dsc_lst = ds.ner_startscript.split(" ")
    dsc_lst.insert(1, ds.ner_name)
    sc = " ".join(dsc_lst)
    if "-F" not in sc:
        sc += " -F /nerdpool/nerdpool/prodigy_recipes/__init__.py"
    return sc


def start_prodigy_server(dataset_id, new=False):
    if new:
        ports = list(
            ProdigyServer.objects.all().values_list("port", flat=True).order_by("port")
        )
        if len(ports) == 0:
            port = 8080
        else:
            port = ports[-1] + 1
        uid = uuid.uuid1()
        ProdigyServer.objects.create(
            port=port, server_hash=uid, dataset_id=int(dataset_id)
        )
        lc = ""
        for s in ProdigyServer.objects.all():
            lc += nginx_loc.format(
                hash=s.server_hash, port=s.port, prodigy_base_url=PRODIGY_BASE_URL
            )
        with open("/nginx/default.conf", "w") as out:
            out.write(nginx_templ.format(loc=lc))
    ds = NerDataSet.objects.get(pk=dataset_id)
    sc = create_prodigy_command(ds)
    if not new:
        port = ds.prodigyserver_set.first().port
        uid = ds.prodigyserver_set.first().server_hash
    base_cmd = [f"PRODIGY_PORT={port} prodigy {sc}"]
    if os.path.isfile(f"/nerdpool/dataset-configs/{dataset_id}/prodigy.json"):
        base_cmd[0] = f"PRODIGY_HOME=/nerdpool/dataset-configs/{dataset_id} {base_cmd[0]}"
    else:
        base_cmd[0] = f"PRODIGY_HOME=/config-nerdpool {base_cmd[0]}"
    Popen(
        base_cmd,
        shell=True,
        stdin=None,
        stdout=None,
        stderr=None,
        close_fds=True,
    )
    return uid


def search_for_server(uid):
    proc_iter = psutil.process_iter(attrs=["pid", "name", "cmdline"])
    ds = ProdigyServer.objects.get(server_hash=uid).dataset
    sc = create_prodigy_command(ds)
    proc = any(sc in " ".join(p.info["cmdline"]) for p in proc_iter)
    return proc


def toggle_prodigy_server(dataset_id):
    ps = ProdigyServer.objects.select_related("dataset").get(dataset_id=dataset_id)
    ds = ps.dataset
    if search_for_server(ps.server_hash):
        proc_iter = psutil.process_iter(attrs=["pid", "name", "cmdline"])
        sc = create_prodigy_command(ds)
        for p in proc_iter:
            if sc in " ".join(p.info["cmdline"]):
                os.kill(p.info["pid"], signal.SIGKILL)
        ps.auto_start = False
        ps.save()
        return False, ps.server_hash
    else:
        uid = start_prodigy_server(ds.pk)
        ps.auto_start = True
        ps.save()
        return True, uid


class ProdigyServers(APIView):
    def post(self, request):
        dataset_id = request.data["dataset"]
        new = request.data.get("new", None)
        toggle = request.data.get("toggle", None)
        if toggle:
            res = toggle_prodigy_server(dataset_id)
            return Response({"server_up": res[0], "uid": res[1]})
        else:
            uid = start_prodigy_server(dataset_id=dataset_id, new=new)
            return Response({"url": f"{uid}.{PRODIGY_BASE_URL}"})

    def get(self, request):
        pk = request.query_params.get("uid", None)
        if pk:
            if ProdigyServer.objects.filter(server_hash=pk).count() == 0:
                raise Http404
            res = search_for_server(pk)
            return Response({"server_up": res, "uid": pk})
        else:
            raise Http404
