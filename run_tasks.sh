#! /bin/bash

source /etc/environment
source /usr/local/bin/virtualenvwrapper.sh

workon service_uploader
python3 ./uploader/manage.py runall