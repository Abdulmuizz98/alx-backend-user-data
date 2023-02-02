#!/usr/bin/env python3
"""Contains the function filtered_logger """

import re
#import typing


def filter_datum(fields: list[str] , redaction: str, message: str, separator: str) -> str:
    """Obsfucate PII in log info"""
    for field in fields:
        reg: str = '(?<={}=).*?(?={})'.format(field, separator)
        message = re.sub(reg, redaction, message)
    return message
