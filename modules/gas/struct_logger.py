#!python3
"""
struct_logger.py
Logging setup to push log messages to Papertrail and stdout. Adapted from
http://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-python-apps/

If no credentials exist for papertrail (or similar), defaults to stdout only
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
    * cfg: A configuration dict with a number of fields
    ** hostname: hostname to display in the Papertrail log stream. Also
                becomes a 'system' in PT within the particular destination
    ** format: format string for logging
    ** date_format: date format string for logging
    ** local_level: log level to send to stdout
    ** remote_address: a two-part list w/ the address and port for remote logs
    ** if the above is missing, only logs to stdout
    """
    # Declare basic logger and wrap in structlog for structured outputs
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger = structlog.wrap_logger(logger, wrapper_class=structlog.BoundLogger)

    # Add filter and define the baseline format
    pt_filter = PapertrailContextFilter(cfg['hostname'], jobname)
    logger._logger.addFilter(pt_filter)
    formatter = logging.Formatter(
        cfg['format'], datefmt=cfg['date_format']
    )

    # Setup the remote logging
    if 'remote_address' in cfg:
        destination_address, destination_port = cfg['remote_address']
        syslog = SysLogHandler(address=(destination_address, destination_port))
        syslog.setFormatter(formatter)
        logger._logger.addHandler(syslog)

    # Setup the local logging
    local_handler = logging.StreamHandler(sys.stdout)
    local_handler.setLevel(cfg['local_level'])
    local_handler.setFormatter(formatter)
    logger._logger.addHandler(local_handler)

    # This line allows subroutine calls to temporarily reference themselves distinctly
    logger = logger.bind(sub='main')

    return logger
