"""
.. module:: service_uploader.core.tasks
   :synopsis: Philo Uploader Core Asynchronous Tasks.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import logging
from pathlib import Path

from django.conf import settings
import requests

from .philo import PhiloExporter
from .notifii import NotifiiExporter
from .SFTPUploader import SFTPUploader
from .advocate import AdvocateExporter, SFTPUploaderAdvocate
from .advocate_models import AdvocateStudentProfile, AdvocateStudentClassSchedule, AdvocateStudentPhoto

logger = logging.getLogger(__name__)


def run_notifii():
    file_list = [settings.NOTIFII_RESIDENT_FILENAME + '.csv']

    clean_temp(file_list)
    exporter = NotifiiExporter(Path(settings.MEDIA_ROOT))
    exporter.export()
    upload_data(settings.SFTP["notifii"], file_list)


def run_philo():
    file_list = [settings.PHILO_ADMIN_FILENAME + '.csv',
                 settings.PHILO_RESIDENT_FILENAME + '.csv']

    clean_temp(file_list)
    exporter = PhiloExporter(Path(settings.MEDIA_ROOT))
    exporter.export()
    upload_data(settings.SFTP["philo"], file_list)


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


def run_all():
    uploader_tasks = {"Philo": run_philo,
                      "Notifii": run_notifii}

    for name, uploader in uploader_tasks.items():
        try:
            uploader()
            log_to_internal(name, True)
        except Exception as e:
            logger.exception(name + " : " + type(e).__name__)
            log_to_internal(name, False)


def clean_temp(file_list):
    for file_ in Path(settings.MEDIA_ROOT).iterdir():
        # Clear all files related to the uploader you are running
        if file_.name in file_list:
            file_.unlink()


def upload_data(sftp_settings, file_list):
    if settings.DEBUG:
        stub_uploader(file_list)
    else:
        uploader = SFTPUploader(sftp_settings)

        for file_ in Path(settings.MEDIA_ROOT).iterdir():
            # Upload all visible files
            if file_.name in file_list:
                uploader.upload_file(str(file_.resolve()), file_.name)


def log_to_internal(uploader_name, success):
    url = settings.INTERNAL_URL + 'uploaders/log_upload/'
    payload = {'uploader':uploader_name,
               'success': success}
    r = requests.post(url, data=payload)
    if r.status_code != 200:
        logger.exception("Failed to log to Internal")


def stub_uploader(file_list):
    for file_ in Path(settings.MEDIA_ROOT).iterdir():
        # Upload all visible files
        if file_.name in file_list:
            print("Uploading " + file_.name)