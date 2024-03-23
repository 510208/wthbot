import json, requests
from fake_useragent import UserAgent
requests.packages.urllib3.disable_warnings()

def ip2carrier(ip):
    ip = str(ip)
    ua = UserAgent()
    headers = {'USER-AGENT': ua.random}
    url = 'http://rdap.apnic.net/ip/' + ip
    webpage = requests.get(url, headers = headers, verify = False)
    html = webpage.text
    try:
        country = json.loads(html)['country']
        carrier = json.loads(html)['name']
    except:
        country = None
        carrier = None
    return(carrier, country)