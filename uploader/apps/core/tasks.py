"""
.. module:: service_uploader.core.tasks
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
    exporter = NotifiiExporter(Path(settings.MEDIA_ROOT))
    exporter.export()
    file_list = [settings.PHILO_ADMIN_FILENAME + '.csv',
                 settings.PHILO_RESIDENT_FILENAME + '.csv']
    upload_data(settings.SFTP["notifii"], file_list)


def run_philo():
    exporter = PhiloExporter(Path(settings.MEDIA_ROOT))
    exporter.export()
    file_list = [settings.NOTIFII_RESIDENT_FILENAME + '.csv']
    upload_data(settings.SFTP["philo"], file_list)


def run_all():
    uploader_tasks = {
        "philo": run_philo,
        "notifii": run_notifii
    }

    clean_temp()
    for uploader in uploader_tasks.values():
        uploader()


def clean_temp():
    for file_ in Path(settings.MEDIA_ROOT).iterdir():
        # Clear all visible files
        if not file_.name.startswith("."):
            file_.unlink()


def upload_data(sftp_settings, file_list):
    uploader = SFTPUploader(sftp_settings)

    for file_ in Path(settings.MEDIA_ROOT).iterdir():
        # Upload all visible files
        if file_.name in file_list:
            uploader.upload_file(str(file_.resolve()), file_.name)
