import json
from common.constants import Constants
from common.utils import Logger, printInfo, printWarning, printError
from common.scheduler.scheduler import JobScheduler
from feed import Feed 
from brain import Brain


if __name__ == '__main__':
  # load config file
  with open(Constants.CONFIG_FILE) as config_file:
    config = json.load(config_file)
    printInfo('Loading config:')
    printInfo(config)

  # initialize logger
  Logger.init(Constants.LOG_FOLDER)

  # initialize trading brain
  Brain.init()
 
  # setup data feed pulling
  scheduler = JobScheduler(
    instance_id = "data_feed",
    job_execution_interval_in_seconds = Constants.FEED_EXECUTION_FREEQUENCY) 
  job_list = []
  job_list.append(Feed(config))
  scheduler.addJobs(job_list)
  printInfo('Setting up data feed pulling. Will execute every ' + str(Constants.FEED_EXECUTION_FREEQUENCY) + ' seconds..')
  scheduler.run()
