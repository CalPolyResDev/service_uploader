"""
.. module:: advocate_uploader.core.models
   :synopsis: Advocate Uploader Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from __future__ import unicode_literals

from django.db.models.base import Model
from django.db.models.fields import CharField, DateField, BinaryField, DecimalField

from .fields import YNBooleanField


class AdvocateStudentProfile(Model):

    guid = CharField(max_length=32, primary_key=True)
    emplid = CharField(max_length=32)
    primary_report_name = CharField(max_length=255)
    primary_first_name = CharField(max_length=30)
    primary_middle_name = CharField(max_length=30)
    primary_last_name = CharField(max_length=30)
    preferred_report_name = CharField(max_length=255)
    preferred_first_name = CharField(max_length=30)
    preferred_middle_name = CharField(max_length=30)
    preferred_last_name = CharField(max_length=30)
    gender_code = CharField(max_length=3)
    gender_descr = CharField(max_length=30)
    birth_date = DateField()
    primary_address_type_code = CharField(max_length=4)
    primary_address_line_1 = CharField(max_length=55)
    primary_address_line_2 = CharField(max_length=55)
    primary_address_city = CharField(max_length=30)
    primary_address_state = CharField(max_length=6)
    primary_address_zipcode = CharField(max_length=12)
    primary_address_country_code = CharField(max_length=3)
    housing_address_line_1 = CharField(max_length=50)
    housing_address_line_2 = CharField(max_length=50)
    housing_address_city = CharField(max_length=50)
    housing_address_state = CharField(max_length=15)
    housing_address_zipcode = CharField(max_length=15)
    email_address = CharField(max_length=256)
    preferred_phone_nbr = CharField(max_length=24)
    plan_1_college_code = CharField(max_length=10)
    plan_1_college_descr = CharField(max_length=50)
    plan_1_major_code = CharField(max_length=10)
    plan_1_major_descr = CharField(max_length=100)
    class_level_code = CharField(max_length=4)
    class_level_ldescr = CharField(max_length=30)
    student_ferpa_flag = YNBooleanField()
    new_student_flag = YNBooleanField()
    admit_term_ldescr = CharField(max_length=30)
    he_units_earned = DecimalField(max_digits=8, decimal_places=3)
    current_term_units_attempted = DecimalField(max_digits=8, decimal_places=3)
    recent_student_flag = YNBooleanField()
    he_gpa = DecimalField(max_digits=8, decimal_places=3)

    def __unicode__(self):
        return self.primary_report_name

    class Meta:
        db_table = '"warehouse"."service_housing_advocate"'
        managed = False
        verbose_name = 'Advocate Student Profile'


class AdvocateStudentClassSchedule(Model):

    emplid = CharField(max_length=11, primary_key=True)  # This is not actually unique... methods that require this will not work correctly
    term_code = CharField(max_length=4)
    class_label = CharField(max_length=29)
    course_catalog_ldescr = CharField(max_length=100)

    mtg1_facility_bldg_code = CharField(max_length=10)
    mtg1_facility_room = CharField(max_length=10)
    mtg1_facility_ldescr = CharField(max_length=30)
    mtg1_start_time = CharField(max_length=10)
    mtg1_end_time = CharField(max_length=10)
    mtg1_days = CharField(max_length=7)

    mtg2_facility_bldg_code = CharField(max_length=10)
    mtg2_facility_room = CharField(max_length=10)
    mtg2_facility_ldescr = CharField(max_length=30)
    mtg2_start_time = CharField(max_length=10)
    mtg2_end_time = CharField(max_length=10)
    mtg2_days = CharField(max_length=7)

    mtg3_facility_bldg_code = CharField(max_length=10)
    mtg3_facility_room = CharField(max_length=10)
    mtg3_facility_ldescr = CharField(max_length=30)
    mtg3_start_time = CharField(max_length=10)
    mtg3_end_time = CharField(max_length=10)
    mtg3_days = CharField(max_length=7)

    mtg4_facility_bldg_code = CharField(max_length=10)
    mtg4_facility_room = CharField(max_length=10)
    mtg4_facility_ldescr = CharField(max_length=30)
    mtg4_start_time = CharField(max_length=10)
    mtg4_end_time = CharField(max_length=10)
    mtg4_days = CharField(max_length=7)

    mtg5_facility_bldg_code = CharField(max_length=10)
    mtg5_facility_room = CharField(max_length=10)
    mtg5_facility_ldescr = CharField(max_length=30)
    mtg5_start_time = CharField(max_length=10)
    mtg5_end_time = CharField(max_length=10)
    mtg5_days = CharField(max_length=7)

    def __unicode__(self):
        return self.emplid

    class Meta:
        db_table = '"warehouse"."service_housing_advocate_class"'
        managed = False
        verbose_name = 'Advocate Student Class Schedule'


class AdvocateStudentPhoto(Model):

    guid = CharField(max_length=32, primary_key=True)
    photo = BinaryField()

    def __unicode__(self):
        return self.guid

    class Meta:
        db_table = '"warehouse"."service_housing_advocate_photo"'
        managed = False
        verbose_name = 'Advocate Student Photo'
