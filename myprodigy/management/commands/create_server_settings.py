from django.core.management.base import BaseCommand, CommandError
from myprodigy.api_views import nginx_loc, nginx_templ, PRODIGY_BASE_URL
from myprodigy.models import ProdigyServer


class Command(BaseCommand):
    help = 'used to recreate the nginx conf for the single instances'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            default="/etc/nginx/conf.d/default.conf",
            help='Full path of the nginx conf file to store',
        )

    def handle(self, *args, **kwargs):
        path = kwargs.get('path', )
        lc = ""
        for s in ProdigyServer.objects.all():
            lc += nginx_loc.format(hash=s.server_hash, port=s.port, prodigy_base_url=PRODIGY_BASE_URL)
        with open(path, 'w') as out:
            out.write(nginx_templ.format(loc=lc))
        self.stdout.write(self.style.SUCCESS('Successfully updated server settings'))
