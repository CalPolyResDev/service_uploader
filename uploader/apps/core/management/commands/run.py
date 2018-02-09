"""
.. module:: service_uploader.core.management.commands.runall
   :synopsis: Commands used to run one or all uploaders.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.management.base import BaseCommand, CommandError

from ...tasks import uploader_tasks

class Command(BaseCommand):
    help = "Runs specified tasks for this application."
    requires_system_checks = True

    def add_arguments(self, parser):
        parser.add_argument("uploader", type=str)

    def handle(self, *args, **options):
        try:
            u = options['uploader']
            uploader_tasks[u]()
        except KeyError:
            raise CommandError('There is no uploader named "%s"' % u)