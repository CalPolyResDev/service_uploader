"""
.. module:: philo_uploader.core.tasks
   :synopsis: Philo Uploader Core Asynchronous Tasks.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging
from pathlib import Path

from django.conf import settings

from .philo import PhiloExporter
from .notifii import NotifiiExporter
from .SFTPUploader import SFTPUploader

logger = logging.getLogger(__name__)

def run_notifii():
    clean_temp()
    exporter = NotifiiExporter(Path(settings.MEDIA_ROOT))
    exporter.export()
    # upload_data(settings.SFTP["notifii"])

def run_philo():
    clean_temp()
    exporter = PhiloExporter(Path(settings.MEDIA_ROOT))
    exporter.export()
    # upload_data(settings.SFTP["philo"])

uploader_tasks = {
    "philo": run_philo,
    "notifii": run_notifii
}

def run_all():
    for uploader in uploader_tasks.values():
        uploader()


def clean_temp():
    for file_ in Path(settings.MEDIA_ROOT).iterdir():
        # Clear all visible files
        if not file_.name.startswith("."):
            file_.unlink()


def upload_data(sftp_settings):
    uploader = SFTPUploader(sftp_settings)

    for file_ in Path(settings.MEDIA_ROOT).iterdir():
        # Upload all visible files
        if not file_.name.startswith("."):
            uploader.upload_file(str(file_.resolve()), file_.name)
