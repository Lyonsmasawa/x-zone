import imp


import urllib.request, json

random_api_url = 'http://quotes.stormconsultancy.co.uk/random.json'

def random_quotes():
    with urllib.request.urlopen(random_api_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

    return get_quotes_response