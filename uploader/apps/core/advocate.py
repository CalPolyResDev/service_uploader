"""
.. module:: advocate_uploader.core.utils
   :synopsis: Advocate Uploader Core Utilities.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import csv
import logging
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import date
from pathlib import Path

from django.conf import settings
from django.utils.encoding import smart_str

from paramiko import Transport, SFTPClient, RSAKey

from .advocate_models import AdvocateStudentProfile

logger = logging.getLogger(__name__)


class AdvocateExporter(object):
    """Exports data either as a csv for model data or png for photo data."""

    def __init__(self, filepath):
        self.filepath = filepath
        logger.debug("Advocate Exporter initiated. Using directory: {filepath}.".format(filepath=str(filepath.resolve())))

    def export_model(self, queryset):
        # Build the path
        filename = queryset.model._meta.verbose_name.lower().replace(" ", "_")
        where = self.filepath.joinpath(str(date.today()) + filename + '.csv')

        logger.debug("Advocate Exporter: Exporting model {filename}. Initiating csv write.".format(filename=filename))

        # Instantiate the writer
        with where.open(mode='w', newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile, dialect='unix')

            # Write headers to CSV file
            headers = []
            for field in queryset.model._meta.fields:
                headers.append(field.name)
            writer.writerow(headers)

            # Write data to CSV file
            for obj in queryset:
                row = []
                for field in headers:
                    if field in headers:
                        val = getattr(obj, field)

                        if type(val) == bool:
                            val = "YES" if val else "NO"

                        row.append(smart_str(val))
                writer.writerow(row)

        logger.debug("Advocate Exporter: Export of model {filename} completed successfully.".format(filename=filename))

    def export_photo(self, queryset):
        # Build the path
        filename = queryset.model._meta.verbose_name.lower().replace(" ", "_")
        where = self.filepath.joinpath(str(date.today()) + filename + '.zip')

        logger.debug("Advocate Exporter: Exporting photos {filename}. Initiating photo write.".format(filename=filename))

        # Create image files
        with ZipFile(str(where), mode='w', compression=ZIP_DEFLATED) as zipfile:
            for obj in queryset:
                student_id = AdvocateStudentProfile.objects.get(guid=obj.guid).emplid
                file_name = str(student_id) + '.jpg'
                file_data = obj.photo
                zipfile.writestr(file_name, file_data)

        logger.debug("Advocate Exporter: Export of photos {filename} completed successfully.".format(filename=filename))


class SFTPUploaderAdvocate(object):
    # this could be refactored with the other SFTP class
    """Uploads files to the advocate data drop using key exchange."""

    def __init__(self):
        private_key = RSAKey.from_private_key_file(filename=str(Path(settings.CONFIG_ROOT).joinpath('advocate_private_key.txt').resolve()), password='a fairly decent passphrase')

        self.transport = Transport((settings.SFTP['advocate']['HOST'], int(settings.SFTP['advocate']['PORT'])))
        self.transport.connect(username=settings.SFTP['advocate']['USER'], pkey=private_key)
        self.connection = SFTPClient.from_transport(self.transport)

        logger.debug("SFTPUploader initiated. Sending files to {host}:{port}".format(host=settings.SFTP['advocate']['HOST'],
                                                                                     port=settings.SFTP['advocate']['PORT']))

    def __del__(self):
        try:
            self.connection.close()
            self.transport.close()
        except AttributeError:
            pass

        logger.debug("SFTPUploader session completed. Connection closed.")

    def upload_file(self, local_filepath, filename):
        logger.debug("SFTPUploader: Uploading file {filepath}".format(filepath=local_filepath))
        self.connection.put(localpath=local_filepath, remotepath='./{filename}'.format(filename=filename))
