import os
import sys
import time
import calendar
import logging
from datetime import datetime


def toUnicode(item):
  if isinstance(item, str):
    item_unicode = unicode(item, errors='ignore')
  else:
    item_unicode = unicode(item)
  return item_unicode

def printInfo(msg):
  Logger.write_info(msg)
  print str(datetime.now()) + '\033[97m [Info] ' + toUnicode(msg) + '\033[0m'
  sys.stdout.flush()

def printWarning(msg):
  Logger.write_warning(msg)
  print str(datetime.now()) + '\033[93m [Warning] ' + toUnicode(msg) + '\033[0m'
  sys.stdout.flush()

def printError(msg):
  Logger.write_error(msg)
  print str(datetime.now()) + '\033[91m [Error] ' + toUnicode(msg) + '\033[0m'
  sys.stdout.flush()

def getFileNameFromPath(file_path):
  tokens = file_path.split('/')
  if len(tokens) == 0:
    return None
  return tokens[-1]

def getFileExtension(file_path):
  filename, file_extension = os.path.splitext(file_path)
  return file_extension


class Logger(object):

  logger = None

  @staticmethod
  def init(log_file_folder, log_level = 'INFO'):
    if not os.path.exists(log_file_folder):
      os.makedirs(log_file_folder)

    logger = logging.getLogger(__name__)
    logger.propagate = False # not log to console
    if log_level == 'INFO':
      logger.setLevel(logging.INFO)
    else:
      logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    formatter.converter = time.gmtime
    log_file_handler = logging.FileHandler(log_file_folder + '/' + time.strftime("%Y_%m_%d__%H_%M_%S", time.gmtime()) + '.log', mode='a')
    log_file_handler.setFormatter(formatter)
    logger.addHandler(log_file_handler)

    Logger.logger = logger

  @staticmethod
  def write_info(message):
    if Logger.logger != None:
      Logger.logger.info(message)

  @staticmethod
  def write_warning(message):
    if Logger.logger != None:
      Logger.logger.warning(message)

  @staticmethod
  def write_error(message):
    if Logger.logger != None:
      Logger.logger.error(message)
