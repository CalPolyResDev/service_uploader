"""
.. module:: notifii_uploader.core.utils
   :synopsis: Notifii Uploader Core Utilities.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import csv
import logging

from django.conf import settings
from django.utils.encoding import smart_str
from dwconnector.exceptions import UnsupportedCommunityException
from dwconnector.models import ResidentProfile
from dwconnector.utils import Resident


logger = logging.getLogger(__name__)


class NotifiiExporter(object):
    """Exports data either as a csv for model data."""

    def __init__(self, filepath):
        self.filepath = filepath
        logger.debug("Notifii Exporter initiated. Using directory: {filepath}.".format(filepath=str(filepath.resolve())))
    
    def export(self):
        self.export_residents()

    def export_residents(self):
        where = self.filepath.joinpath(settings.NOTIFII_RESIDENT_FILENAME + '.csv')

        # Build the resident list
        logger.debug("Notifii Exporter: Exporting residents. Collecting resident data.")

        students = ResidentProfile.objects.filter(on_campus_resident_flag__iexact='Y')

        residents = []
        for resident in students:
            try:
                residents.append(Resident(principal_name=resident.email_address))
            except UnsupportedCommunityException:
                pass
            except AttributeError:
                logger.exception(resident)

        logger.debug("Notifii Exporter: Exporting residents. Initiating csv write.")

        # Instantiate the writer
        with where.open(mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='unix')

            # Write data to CSV file
            for resident in residents:
                row = []
                row.append(smart_str(resident.primary_first_name))
                row.append(smart_str(resident.primary_last_name))
                row.append(smart_str(resident.address))
                row.append(smart_str(resident.email))
                row.append(smart_str(resident.cell_phone))
                writer.writerow(row)

        logger.debug("Notifii Exporter: Export of residents completed successfully.")
