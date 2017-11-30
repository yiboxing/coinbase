class Constants:
  CONFIG_FILE = 'config.cfg'
  LOG_FOLDER = './log'
  ERROR_EMAIL_RECIPIENT = ['me@xingyibo.com']
  FEED_EXECUTION_FREEQUENCY = 1 # in seconds
  CURL_TIMEOUT = 60
  API_KEY_IN_CFG = 'api_key'
  API_SECRET = 'api_secret'
  API_PASSPHRASE_IN_CFG = 'api_passphrase'
  GDAX_ROOT_URL_IN_CFG = 'gdax_root_url'
  PRODUCT_ID = 'product_id'



class ApiKey:
  STATUS        = 'status'
  ID            = 'id'
  PRICE         = 'price'


class ApiValue:
  NULL        = ''


class ApiErrorCode:
  NO_ERROR  = 0
#   SERVER_CONNECTION_ERROR = 10000
#   INVALID_RESPONSE_FORMAT = 10001

class ApiStatus:
  OK      = 'OK'
  SUCCESS = 'SUCCESS'
  ERROR   = 'ERROR'