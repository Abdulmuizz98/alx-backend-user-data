#!/usr/bin/env python3
""" Contains the function filtered_logger that obfuscate PII in
log info for privacy"""

import re
import logging


def filter_datum(fields: list[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obsfucate PII in log info for privacy"""
    for field in fields:
        reg: str = '(?<={}=).*?(?={})'.format(field, separator)
        message = re.sub(reg, redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        """Initializes the sub class RedactingFormatter """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with the function filter_datum """
        record.msg = record.msg.replace(';', '; ')
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
