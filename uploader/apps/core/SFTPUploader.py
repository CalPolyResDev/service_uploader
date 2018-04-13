import logging
from paramiko import Transport, SFTPClient

logger = logging.getLogger(__name__)


class SFTPUploader(object):
    """Uploads files to (s)ftp"""

    def __init__(self, sftp_settings):
        self.transport = Transport((sftp_settings['HOST'], int(sftp_settings['PORT'])))
        self.transport.connect(username=sftp_settings['USER'], password=sftp_settings['PASSWORD'])
        self.connection = SFTPClient.from_transport(self.transport)

        logger.debug("SFTPUploader initiated. Sending files to {host}:{port}".format(host=sftp_settings['HOST'],
                                                                                     port=sftp_settings['PORT']))

    def __del__(self):
        try:
            self.connection.close()
            self.transport.close()
        except AttributeError:
            pass

        logger.debug("SFTPUploader session completed. Connection closed.")

    def upload_file(self, local_filepath, filename):
        logger.debug("SFTPUploader: Uploading file {filepath}".format(filepath=local_filepath))
        try:
            self.connection.remove(path='./{filename}'.format(filename=filename))
        except IOError:
            pass
        self.connection.put(localpath=local_filepath, remotepath='./{filename}'.format(filename=filename))
