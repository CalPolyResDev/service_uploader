"""
.. module:: philo_uploader.core.management.commands.runall
   :synopsis: Philo Uploader Core Management Commands.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.management.base import BaseCommand

from ...tasks import run_all


class Command(BaseCommand):
    help = "Runs all tasks for this application."
    requires_system_checks = True

    def handle(self, *args, **options):
        print("Initiating tasks.")
        run_all()
        print("Tasks complete.")
