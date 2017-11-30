
import os
import sys
sys.path.append('../')

from common.utils import printInfo, printWarning, printError
from common.http.request import HttpRequest
from common.constants import Constants, ApiKey, ApiValue


class Products(object):

  def __init__(self, service_root_url):
    self._http_request = HttpRequest(service_root_url) 

  def get(self):
    params = {
    }
    response = self._http_request.get('/products', params)
    return response


class ProductPriceTicker(object):

  def __init__(self, service_root_url):
    self._http_request = HttpRequest(service_root_url) 

  def get(self, product_id):
    params = {
    }
    response = self._http_request.get('/products/' + product_id + '/ticker', params)
    return response

    # self._key = config[Constants.API_KEY_IN_CFG]
    # self._passphrase = config[Constants.PASSPHRASE_IN_CFG]

