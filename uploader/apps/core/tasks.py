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
from .advocate import AdvocateExporter, SFTPUploaderAdvocate
from .advocate_models import AdvocateStudentProfile, AdvocateStudentClassSchedule, AdvocateStudentPhoto

logger = logging.getLogger(__name__)

def run_notifii():
    clean_temp()
    exporter = NotifiiExporter(Path(settings.MEDIA_ROOT))
    exporter.export()
    upload_data(settings.SFTP["notifii"])

def run_philo():
    clean_temp()
    exporter = PhiloExporter(Path(settings.MEDIA_ROOT))
    exporter.export()
    upload_data(settings.SFTP["philo"])

def run_advocate():
    # Initiate exporter
    exporter = AdvocateExporter(Path(settings.MEDIA_ROOT))
    # Generate querysets
    profiles = AdvocateStudentProfile.objects.all()
    class_schedules = AdvocateStudentClassSchedule.objects.all()
    photos = AdvocateStudentPhoto.objects.all()
    # Build files for upload
    exporter.export_model(profiles)
    exporter.export_model(class_schedules)
    exporter.export_photo(photos)
    
    # upload_data(settings.SFTP["advocate"])

uploader_tasks = {
    "philo": run_philo,
    "notifii": run_notifii,
    "advocate": run_advocate
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
