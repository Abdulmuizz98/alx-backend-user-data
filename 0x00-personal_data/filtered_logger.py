#!/usr/bin/env python3
""" Contains the function filtered_logger that obfuscate PII in
log info for privacy"""

import re
import logging
from typing import List
from mysql import connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obsfucate PII in log info for privacy"""
    for field in fields:
        reg: str = '(?<={}=).*?(?={})'.format(field, separator)
        message = re.sub(reg, redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the sub class RedactingFormatter """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with the function filter_datum """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger('user_data').setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connector.MySQLConnection:
    """Returns a connection to a MySQL database """
    from os import getenv
    USER: str = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    PASSWD: str = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    HOST: str = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    DB: str = getenv('PERSONAL_DATA_DB_NAME')

    cnx = connector.connect(user=USER, password=PASSWD, host=HOST, database=DB)
    return cnx
