#! /bin/bash

source /etc/environment
source /usr/local/bin/virtualenvwrapper.sh

workon uploader_project
python3 ./uploader/manage.py runall