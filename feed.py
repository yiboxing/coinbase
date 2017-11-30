import json
from common.constants import Constants, ApiKey, ApiValue
from common.utils import Logger, printInfo, printWarning, printError
from api.gdax import Products, ProductPriceTicker
from brain import Brain


class Feed(object):

  def __init__(self, config):
    #self.products = Products(config[Constants.GDAX_ROOT_URL_IN_CFG])
    self.product_id = config[Constants.PRODUCT_ID];
    self.product_price_ticker = ProductPriceTicker(config[Constants.GDAX_ROOT_URL_IN_CFG])

  def execute(self):
    # get_product_response = self.products.get();
    # printInfo(get_product_response)
    # eth = None
    # for product in get_product_response:
    #   if product[ApiKey.ID] == 'ETH-USD':
    #     eth = product
    product_price_ticker_response = self.product_price_ticker.get(self.product_id)
    price = float(product_price_ticker_response[ApiKey.PRICE])
    # update to brain
    Brain.updateCurrentPrice(price)




