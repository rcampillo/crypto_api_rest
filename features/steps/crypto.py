from behave import given, when, then
import requests

api_endpoints = {}
response_results = {}
response_codes = {}
response_texts = {}
response_errors = {}
api_url=None

@given(u'I set required REST API url')
def step_impl(context):
    global api_url
    api_url = 'https://api.kraken.com'

# START GET Scenario
@given(u'I Set GET posts api endpoint "{id}"')
def step_impl(context, id):
    api_endpoints['GET'] = api_url + id
    print('url :'+api_endpoints['GET'])


@when(u'Send POST HTTP request once rcampillo auth has been set')
def step_impl(context):

    # API key and secret
    api_key = "2Awp1WUjOBzST8Rss7XMpWWeqHzkKvW+ul2uxgy/wGbvcRRHw9neFeAh"
    api_sec = "Ovzqd0lSoSDTuI5vSUj8XkIb9ciIsqTl/Y0ysRu4vgGRvrXZRmuH+PajmVd3Y6EpRaWhMq20tnmjFqp+4QowOw=="

    def get_signature(urlpath, data, secret):
        import urllib.parse
        import hashlib
        import hmac
        import base64
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    # Attaches auth headers and returns results of a POST request
    def crypto_request(uri_path, data, api_key, api_sec):
        headers = {'API-Key': api_key, 'API-Sign': get_signature(uri_path, data, api_sec)}
        req = requests.post(api_endpoints['GET'], headers=headers, data=data)
        return req

    import time
    # Construct the request and print the result
    # Request open orders from a specific user (mine in this case) with 2 factor authentication requirements '/0/private/OpenOrders'
    response = crypto_request(api_endpoints['GET'][len(api_url)::], {"nonce": str(int(1000 * time.time())), "trades": True}, api_key,
                          api_sec)
    # extracting response text
    response_texts['GET'] = response.text
    response_json = response.json()

    try:
        response_results['GET'] = response_json["result"]
    except KeyError:
        response_errors['GET'] = response_json["error"]
    # extracting response status_code
    statuscode = response.status_code
    response_codes['GET'] = statuscode


@when(u'Send GET HTTP request')
def step_impl(context):
    response = requests.get(url=api_endpoints['GET'])
    # extracting response text
    response_texts['GET']=response.text
    response_json = response.json()

    try:
        response_results['GET'] = response_json["result"]
    except KeyError:
        response_errors['GET'] = response_json["error"]
    # extracting response status_code
    statuscode = response.status_code
    response_codes['GET'] = statuscode

@then(u'I receive valid HTTP response code 200 for "{request_name}"')
def step_impl(context,request_name):
    print('Get rep code for '+request_name+':'+ str(response_codes[request_name]))
    assert response_codes[request_name] == 200

@then(u'Response BODY "{request_name}" is non-empty')
def step_impl(context,request_name):
    print('request_name: '+request_name)
    print(response_texts)
    assert response_texts[request_name] is not None

@then(u'Response ERROR "{request_name}" is non-empty')
def step_impl(context,request_name):
    print('request_name: '+request_name)
    print(response_errors)
    assert response_errors[request_name] is not None