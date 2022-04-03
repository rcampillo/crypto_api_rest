import requests
import urllib.parse
import hashlib
import hmac
import base64
import time


def test_server_time():
  # First endpoint is Time, which provides server time info

  resp = requests.get('https://api.kraken.com/0/public/Time')

  # Check received response, status is equal to 200 and provided value
  assert resp.text is not None, "Request response body is None"
  assert resp.status is 200, "Request response status is not 200"
  print(f" Server time is {resp.json()["result"]["unixtime"]}")
  
def test_BTC_USD_pair():
  # Build proper endpoint request, filling pair variable with pair value 
  resp = requests.get('https://api.kraken.com/0/public/AssetPairs?pair=XXBTZUSD')
  # Check received response, status is equal to 200 and provided value
  assert resp.text is not None, "Request response body is None"
  assert resp.status is 200, "Request response status is not 200"
  print(f"Pair BTC/USD info is {resp.json()["result"]["XXBTZUSD"]}")
  
def test_open_orders_rcampillo():  
  # API key and secret
  api_url = "https://api.kraken.com"
  # It's not better strategy to share my private info with you, but I've registered user just to this test and I'm not going to operate in cryptocurrency
  api_key = "2Awp1WUjOBzST8Rss7XMpWWeqHzkKvW+ul2uxgy/wGbvcRRHw9neFeAh"
  api_sec = "Ovzqd0lSoSDTuI5vSUj8XkIb9ciIsqTl/Y0ysRu4vgGRvrXZRmuH+PajmVd3Y6EpRaWhMq20tnmjFqp+4QowOw=="


  def get_signature(urlpath, data, secret):
      postdata = urllib.parse.urlencode(data)
      encoded = (str(data['nonce']) + postdata).encode()
      message = urlpath.encode() + hashlib.sha256(encoded).digest()
  
      mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
      sigdigest = base64.b64encode(mac.digest())
      return sigdigest.decode()


  # Attaches auth headers and returns results of a POST request
  def crypto_request(uri_path, data, api_key, api_sec):
      headers = {'API-Key': api_key, 'API-Sign': get_signature(uri_path, data, api_sec)}
      req = requests.post((api_url + uri_path), headers=headers, data=data)
      return req
  # Construct the request and print the result
  # Request open orders from a specific user (mine in this case) with 2 factor authentication requirements
  resp = crypto_request('/0/private/OpenOrders', {"nonce": str(int(1000 * time.time())), "trades": True}, api_key,
                        api_sec)

  # Check received response, status is equal to 200 and provided value
  assert resp.text is not None, "Request response body is None"
  assert resp.status is 200, "Request response status is not 200"
  print(f"Rcampillo open orders are {resp.json()["result"]["open"]}")
  
