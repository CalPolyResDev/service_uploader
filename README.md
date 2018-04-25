# service_uploader
Cron uploader for Philo, Notifiii, etc.

## Setup
Make sure an `.env` file containing the contents from [`UPLOADER.env`](https://code.its.calpoly.edu/projects/UHSC/repos/environment_files/browse/UPLOADER.env) exists at the repo's root dir. (use symlink?)

Then setup the environement:
```
source /etc/environment
source /usr/local/bin/virtualenvwrapper.sh

workon service_uploader
```

## Running all uploaders
To run all uploaders: `python3 ./uploader/manage.py runall`

This will take a LONG TIME (10-30 minutes) appear to be stuck...until it's not.

## Running one uploader
`python3 ./uploader/manage.py run NAME_OF_UPLOADER`

ex:
`python3 ./uploader/manage.py run philo`
