

class SuspendExecutionException(Exception):

  def __init__(self, additional_info = {}):
    super(SuspendExecutionException, self).__init__()
    self._additional_info = additional_info

  def __str__(self):
    return 'Fatal error! will suspend execution...'

  def _getMessage(self, suspended_process_name):
    return '%s error! Will suspend execution (%s)'%(\
      suspended_process_name, str(self._additional_info))





