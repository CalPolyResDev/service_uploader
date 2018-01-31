"""
.. module:: philo_uploader.core.tasks
   :synopsis: Philo Uploader Core Asynchronous Tasks.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging
from pathlib import Path

from django.conf import settings

import philo
import notifii
import SFTPUploader

logger = logging.getLogger(__name__)


def run_all():
    run_philo()
    run_notifii()

def run_notifii():
    clean_temp()
    exporter = notifii(Path(settings.MEDIA_ROOT))
    fetch_data(exporter)
    upload_data(settings.SFTP["notifii"])

def run_philo():
    clean_temp()
    exporter = philo(Path(settings.MEDIA_ROOT))
    fetch_data(exporter)
    upload_data(settings.SFTP["philo"])


def clean_temp():
    for file_ in Path(settings.MEDIA_ROOT).iterdir():
        # Clear all visible files
        if not file_.name.startswith("."):
            file_.unlink()


def fetch_data(exporter):
    # Build files for upload
    exporter.export_residents()
    exporter.export_admins()


def upload_data(sftp_settings):
    uploader = SFTPUploader(sftp_settings)

    for file_ in Path(settings.MEDIA_ROOT).iterdir():
        # Upload all visible files
        if not file_.name.startswith("."):
            uploader.upload_file(str(file_.resolve()), file_.name)
