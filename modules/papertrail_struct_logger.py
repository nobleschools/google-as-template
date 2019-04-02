#!python3
"""
papertrail_struct_logger.py
Logging setup to push log messages to Papertrail and stdout. Adapted from
http://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-python-apps/
"""

import logging
from logging.handlers import SysLogHandler
import sys

import structlog


class PapertrailContextFilter(logging.Filter):

    def __init__(self, hostname, jobname, *args, **kwargs):
        # To conform to log coloration on PT, which splits by whitespace
        self.hostname = hostname.replace(" ", "")
        self.jobname = jobname.replace(" ", "")
        super().__init__(*args, **kwargs)

    def filter(self, record):
        record.hostname = self.hostname
        record.jobname = self.jobname
        return True


def get_logger(jobname, cfg):
    """
    Creates a logger with the `PapertrailContextFilter`, pointed at an
    address and port of a PT log destination.
    Positional arguments:
    * jobname: job name to display in the Papertrail log stream
    * cfg: A configuration dictionary with a number of fields
    ** log_hostname: hostname to display in the Papertrail log stream. Also
                becomes a 'system' in PT within the particular destination
    ** log_format: format string for logging
    ** log_date_format: date format string for logging
    ** log_address: a two-part list w/ the address and port for remote logs
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger = structlog.wrap_logger(logger, wrapper_class=structlog.BoundLogger)

    pt_filter = PapertrailContextFilter(cfg['log_hostname'], jobname)
    logger._logger.addFilter(pt_filter)
    destination_address, destination_port = cfg['log_address']
    syslog = SysLogHandler(address=(destination_address, destination_port))
    formatter = logging.Formatter(
        cfg['log_format'], datefmt=cfg['log_date_format']
    )
    syslog.setFormatter(formatter)
    logger._logger.addHandler(syslog)
    local_handler = logging.StreamHandler(sys.stdout)
    local_handler.setFormatter(formatter)
    logger._logger.addHandler(local_handler)

    return logger

    # return (destination, port)


if __name__ == "__main__":
    pass
