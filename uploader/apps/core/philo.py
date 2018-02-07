"""
.. module:: philo_uploader.core.utils
   :synopsis: Philo Uploader Core Utilities.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import csv
import logging

from django.conf import settings

from ldap_groups.groups import ADGroup
from paramiko import Transport, SFTPClient
from dwconnector.exceptions import UnsupportedCommunityException
from dwconnector.models import ResidentProfile
from dwconnector.utils import Resident


logger = logging.getLogger(__name__)

ADMIN_FILENAME = "philo_admin"
RESIDENT_FILENAME = "usernames_emails"


class PhiloExporter(object):
    """Exports data either as a csv for model data or png for photo data."""

    def __init__(self, filepath):
        self.filepath = filepath
        logger.debug("Philo Exporter initiated. Using directory: {filepath}.".format(filepath=str(filepath.resolve())))

    def export(self):
        self.export_admins()
        self.export_residents()

    def export_admins(self):
        # Build the path str(date.today()) +
        where = self.filepath.joinpath(ADMIN_FILENAME + '.csv')

        # Build the admin list
        logger.debug("Philo Exporter: Exporting admins. Collecting admin data.")

        admin_list = ADGroup(settings.ADMIN_AD_GROUP).get_tree_members()

        logger.debug("Philo Exporter: Exporting admins. Initiating csv write.")

        # Instantiate the writer
        with where.open(mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='unix')

            # Write data to CSV file
            for admin in admin_list:
                row = []
                for attribute in settings.LDAP_GROUPS_ATTRIBUTE_LIST:
                    row.append(admin[attribute])
                writer.writerow(row)

        logger.debug("Philo Exporter: Export of admins completed successfully.")

    def export_residents(self):
        where = self.filepath.joinpath(RESIDENT_FILENAME + '.csv')

        # Build the resident list
        logger.debug("Philo Exporter: Exporting residents. Collecting resident data.")

        students = ResidentProfile.objects.filter(on_campus_resident_flag__iexact='Y')

        residents = []
        for resident in students:
            try:
                residents.append(Resident(principal_name=resident.email_address))
            except UnsupportedCommunityException:
                pass
            except AttributeError:
                logger.exception(resident)

        logger.debug("Philo Exporter: Exporting residents. Initiating csv write.")

        # Instantiate the writer
        with where.open(mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='unix')

            # Write data to CSV file
            for resident in residents:
                row = []
                row.append(resident.principal_name.replace("@calpoly.edu", ""))
                row.append(resident.principal_name)
                writer.writerow(row)

        logger.debug("Philo Exporter: Export of residents completed successfully.")