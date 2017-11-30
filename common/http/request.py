import traceback
import sys
import json
import subprocess
import urllib
import base64
from common.constants import Constants
from response import HttpSuccess, HttpError

class HttpMethod:
  GET  = 'GET'
  PUT  = 'PUT'
  POST = 'POST'
  DELETE = 'DELETE'


class CurlLib(object):
  
  def setAuthentication(self, key, passphrase): 
    self._key = key
    self._passphrase = passphrase 
     
  def get(self, url, data):
    return self._connect(HttpMethod.GET, url, data)

  def post(self, url, data):
    return self._connect(HttpMethod.POST, url, data)

  def put(self, url, data):
    return self._connect(HttpMethod.PUT, url, data)

  def _connect(self, method, url, data):
    # GET
    if method == HttpMethod.GET:
      if (not data) or (len(data.keys()) == 0): 
        full_url = url 
      else:    
        full_url = url + '?' + urllib.urlencode(data)
      curl_cmd = 'curl "%s"'%(full_url)

    # DELETE
    elif (method == HttpMethod.DELETE):
      # Need to add "X-Auth-User" header for DELETE request  
      json_str = json.dumps(data)
      rectified_json_str = json_str.replace("'", '\u0027') 
      if data.has_key('user_id'):  
        curl_cmd = """curl -X %s -H "Content-Type: application/json" -H "X-Auth-User: %s" -H "X-Auth-Token: %s" "%s" -d '%s'"""%(method, data['user_id'], self._token, url, rectified_json_str)  
      else: 
        curl_cmd = """curl -X %s -H "Content-Type: application/json" "%s" -d '%s'"""%(method, url, rectified_json_str) 

    # POST, PUT
    elif (method == HttpMethod.POST) or (method == HttpMethod.PUT):  
      # Need to add "X-Auth-Token" header for POST and PUT request  
      json_str = json.dumps(data) 
      rectified_json_str = json_str.replace("'", '\u0027')
      if data.has_key('user_id'):
        curl_cmd = """curl -X %s -H "Content-Type: application/json" -H "X-Auth-User: %s" -H "X-Auth-Token: %s"  "%s" -d '%s'"""%(method, data['user_id'], self._token, url, rectified_json_str)  
      else:
        try:
          curl_cmd = """curl -X %s -H "Content-Type: application/json" "%s" -d '%s'"""%(method, url, rectified_json_str)
        except:
          curl_cmd_str = """curl -X {0} -H "Content-Type: application/json" "{1}" -d '{2}'""".format(method, url, rectified_json_str)
          curl_cmd = unicode(curl_cmd_str, errors='ignore') 
    
    else:
      raise Exception('Http method not supported! method: %s'%(method))

    curl_cmd += ' -m %d'%(Constants.CURL_TIMEOUT)
    proc = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    return out

class HttpRequest:

  def __init__(self, base_url):
    self._base_url = base_url
    self._http_connect_lib = CurlLib()
    
  def setAuthentication(self, key, passphrase):
    self._key = key
    self._passphrase = passphrase
    self._http_connect_lib.setAuthentication(key, passphrase)

  def get(self, rel_path, params):
    return self._connect(HttpMethod.GET, rel_path, params)
    
  def post(self, rel_path, params):
    return self._connect(HttpMethod.POST, rel_path, params)
  
  def put(self, rel_path, params):
    return self._connect(HttpMethod.PUT, rel_path, params)

  def sign(self, method, rel_path, data):
    time_stamp = time.time()
    #  str(time_stamp) + method + rel_path + data
    # sign_key = base64.b64decode(self._key)
    # hmac = 

  def _connect(self, http_method, rel_path, params):
    url  = self._base_url + rel_path
    data = params

    if http_method == HttpMethod.GET:
      connect = self._http_connect_lib.get
    elif http_method == HttpMethod.PUT:
      connect = self._http_connect_lib.put
    elif http_method == HttpMethod.POST:
      connect = self._http_connect_lib.post
    else:
      return None # not supported
    
    success, raw_response_json = False, None
    try:
      raw_response_str = connect(url = url, data = data)
      raw_response_json = json.loads(raw_response_str)
      success = True
    except Exception as e:
      traceback.print_exc()
      sys.stdout.flush()
      pass
    return raw_response_json

