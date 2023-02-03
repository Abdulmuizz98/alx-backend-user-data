#!/usr/bin/env python3

from filtered_logger import get_logger
get_logger = __import__('filtered_logger').get_logger

log = get_logger()
log.error("Boy")
