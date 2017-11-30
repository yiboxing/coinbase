import time
from common.utils import Logger, printInfo, printWarning, printError

# the brain to decide when to buy and sell
class Brain(object):

  current_price = 0.0
  position = False # whether or not holding a product
  tick_history_start_time = 0
  tick_history = []
  one_minute_history = []

  @classmethod
  def init(cls):
    printInfo('TradingBrain initialized')

  @classmethod
  def updateCurrentPrice(cls, new_price):
    cls.current_price = new_price
    
    if len(cls.tick_history) == 0:
      cls.tick_history_start_time = time.time()
    cls.tick_history.append(cls.current_price)

    # add current price to one minue history
    if time.time() - cls.tick_history_start_time > 60:
      if len(cls.tick_history) > 0:
        total = 0;
        for price_tick in cls.tick_history:
          total += price_tick
        one_minute_average = total / len(cls.tick_history)
        cls.updateOneMinuteHistory(one_minute_average)
        cls.tick_history = []

  @classmethod
  def updateOneMinuteHistory(cls, one_minute_average):
    printWarning('One minute average: ' + str(one_minute_average))
    cls.one_minute_history.append(one_minute_average)

    # check buy in signal
    number_of_periods = 10
    buy_threshold = 0.06
    if not cls.position:
      buy_threshold_check = 0
      if len(cls.one_minute_history) > number_of_periods:
        for index in range(len(cls.one_minute_history) - number_of_periods, len(cls.one_minute_history)):
          delta = ((cls.one_minute_history[index] / cls.one_minute_history[index - 1]) - 1.0) * 100
          if delta >= buy_threshold:
            buy_threshold_check += 1
          printInfo('delta: ' + str(index) + ' vs ' + str(index - 1) + ' => '  + str(delta) + '%' + ' buy_threashold_check: ' + str(buy_threshold_check))

      if (buy_threshold_check == number_of_periods): # all checks have met 
        # send buy in signal
        printError('BUY BUY BUY')






        











