import sys

from loguru import logger

custom_format = "<green>{level}</green>:\t  <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - {message}"
logger.remove()
logger.add(sink=sys.stdout, format=custom_format)
