#! /bin/bash

source /etc/environment
source /usr/local/bin/virtualenvwrapper.sh

workon philo_uploader_project
if [ ! -f .update_lock ]; then
    touch .update_lock
    GITOUTPUT=$(git pull 2> /dev/null)
    SUCCESS=$?
    echo $GITOUTPUT | grep 'Already up-to-date.' > /dev/null
    UPDATED=$?

    if (( $UPDATED == 1 && $SUCCESS == 0 )); then    
    echo $GITOUTPUT
    pip3 install -U pip wheel setuptools
    pip3 install -U -r requirements.txt 
    touch conf/uwsgi.ini
    fi
    rm .update_lock
fi