#!/usr/bin/env python3
"""Contains the function filtered_logger """

import re


def filter_datum(fields, redaction, message, separator):
    """Obsfucate PII in log info"""
    for field in fields:
        reg = '(?<={}=).*?(?={})'.format(field, separator)
        message = re.sub(reg, redaction, message)
    return message
