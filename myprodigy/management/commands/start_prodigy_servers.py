from django.core.management.base import BaseCommand, CommandError
from myprodigy.api_views import start_prodigy_server
from myprodigy.models import ProdigyServer


class Command(BaseCommand):
    help = "Starts all servers that are set to On"

    def handle(self, *args, **kwargs):
        for server in ProdigyServer.objects.filter(auto_start=True):
            start_prodigy_server(server.dataset_id, new=False)
