from datetime import datetime
from bs4 import BeautifulSoup
import requests
from urllib import parse
import json


def magti_bil(co__username, co__password , now):
    session = requests.Session()
    session.cookies.get_dict()

    frst_post = session.post("https://userarea.magticom.ge", data={'UserName': co__username, 'Password': co__password})

    frst_view = BeautifulSoup(frst_post.text, 'lxml')

    attrs = {}
    for vals in frst_view.findAll('input'):
        attrs[vals['id'][3:]] = vals['value']

    attrs['TabIndex'] = '0'

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6,ka;q=0.4',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '84',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '__utma=142200110.405086356.1478026025.1478467079.1481496629.3; _ga=GA1.2.405086356.1478026025; '
                  'ASP.NET_SessionId=%(ASP.NET_SessionId)s' % session.cookies.get_dict(),
        'Host': 'userarea.magticom.ge',
        'Origin': 'https://userarea.magticom.ge',
        'Pragma': 'no-cache',
        'Referer': '%s' % frst_post.url,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    scnd_post = requests.post('https://userarea.magticom.ge/Services/LoadTab', data=parse.urlencode(attrs).encode(),
                              headers=headers)

    scnd_view = BeautifulSoup(scnd_post.text, 'html.parser')

    eaten = json.loads(scnd_view.text)

    third_view = BeautifulSoup(eaten['Data'], 'html.parser')

    dirty_p = third_view.findAll('p')
    clean_p = []

    for clean in dirty_p:
        clean_p.append(clean.text)

    latest_dict = dict([(k, v) for k, v in zip(clean_p[::2], clean_p[1::2])])

    pay_day = latest_dict['გათიშვის თარიღი']

    pay_day = datetime.strptime(pay_day, "%d.%m.%Y")

    now = datetime.strptime(now, "%d.%m.%Y")

    time = pay_day - now

    ret_list = ['CO/Magti',str(time)[:7], latest_dict['ბალანსი']]

    return ret_list