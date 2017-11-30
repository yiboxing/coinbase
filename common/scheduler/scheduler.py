import sys
import traceback
import logging
import schedule, time
from common.constants import Constants
from datetime import datetime
from common.exceptions import SuspendExecutionException
from common.sendmail import EmailClient
from common.utils import printInfo, printWarning, printError
from threading import Thread, Lock


class SchedulerLogFilter(logging.Filter):
  def filter(self, record):
    return not 'maximum number of running instances reached' in record.msg


class JobScheduler:

  def __init__(self, instance_id, job_execution_interval_in_seconds, max_job_invocation_count = None):
    logging.basicConfig()
    logging.getLogger("apscheduler.scheduler")\
           .addFilter(SchedulerLogFilter())

    self._instance_id = instance_id
    
    schedule.every(job_execution_interval_in_seconds)\
            .seconds\
            .do(self._executeJobs)

    if max_job_invocation_count is not None:
      self._max_job_invocation_count = int(max_job_invocation_count)
    else:
      self._max_job_invocation_count = None
    self._job_invocation_count = 0
    
    self._mutex = Lock()
    self._job_list = []
    self._enableJobs()

  def run(self):
    self._executeJobs()
    try:
      while True:
          schedule.run_pending()
          
          if (self._max_job_invocation_count is not None) and \
             (self._job_invocation_count >= self._max_job_invocation_count):
            printInfo('Max job invocation count reached. Exiting...')
            break

          time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
      pass

  def clearJobs(self, job):
    self._job_list = []

  def addJob(self, job):
    self._job_list.append(job)

  def addJobs(self, job_list):
    self._job_list += job_list
  
  def _enableJobs(self):
    self._mutex.acquire()
    self._jobs_enabled = True
    self._mutex.release()

  def _disableJobs(self):
    self._mutex.acquire()
    self._jobs_enabled = False
    self._mutex.release()
  
  def _executeJobs(self):
    if self._jobs_enabled:
      self._disableJobs()
      for job in self._job_list:
        try:
          
          job.execute()

        except SuspendExecutionException as see:
          self._sendOutJobSuspensionNotification(see)
          printInfo('Shutting down scheduler...')
          self._shutdown()

        except Exception as e:
          self._sendOutExceptionNotification(e)
          pass
        
        self._job_invocation_count += 1
    
      self._enableJobs()

  def _sendOutExceptionNotification(self, exception):
    stack_trace = traceback.format_exc()
    timestamp_str = str(datetime.now().date())
    subject    = '[Warning] %s job exception (%s)!'%(self._instance_id, timestamp_str)
    printError('Job execution failed, suspend job: ' + str(exception))
    printError('Stack Trace: \n' + stack_trace)
    self._sendmail(subject, exception, stack_trace)
    printInfo('Email notification sent out.')   

  def _sendOutJobSuspensionNotification(self, exception):
    stack_trace = traceback.format_exc()
    timestamp_str = str(datetime.now().date())
    subject    = '[Error] %s job suspended (%s)!'%(self._instance_id, timestamp_str)
    printError('Job execution failed, suspend job: ' + str(exception))
    printError('Stack Trace: \n' + stack_trace)
    self._sendmail(subject, exception, stack_trace)
    printInfo('Email notification sent out.')   

  def _shutdown(self):
    exit(1)

  def _sendmail(self, subject, exception, stack_trace):
    recipient_email = Constants.ERROR_EMAIL_RECIPIENT
    email_body = '\nHi there,\n\n'
    email_body += 'We\'ve got a problem!\n\n'
    email_body += 'Instance ID: %s\n\nException: %s \n\n Stack Trace: %s \n\n'%(\
      self._instance_id, str(exception), stack_trace)
    email_body += 'Please... fix my problem at your earliest convenience :) Thank you!\n\n'
    email_body += 'Cheers!\nSliver match data scraper\n\n'

    printInfo('Sending out email...')
    printInfo('Recipient: %s'%(", ".join(recipient_email)))
    printInfo('Subject: %s'%(subject))
    printInfo('Body: \n%s'%(email_body))

    EmailClient.send(
      recipient_email = recipient_email,
      subject         = subject,
      body            = email_body
    )