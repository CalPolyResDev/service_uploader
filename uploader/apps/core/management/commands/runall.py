"""
.. module:: service_uploader.core.management.commands.runall
   :synopsis: Uploader Core Management Commands.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.management.base import BaseCommand

from ...tasks import run_all


class Command(BaseCommand):
    help = "Runs all tasks for this application."
    requires_system_checks = True

    def handle(self, *args, **options):
        print("Running uploaders. This will take a while...")
        run_all()
        print("Tasks complete.")
