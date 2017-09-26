from datetime import datetime
from bs4 import BeautifulSoup
import requests


def telasi_bil (ID,now):
    frst_post = requests.get('http://my.telasi.ge/customers/info/%s' % ID)
    soup = BeautifulSoup(frst_post.text,'html.parser')

    result = []
    for code in soup.findAll('code'):
        result.append(code.text)


    result = [float(i) for i in result[1:4]]


    pay_day_water_filter = []

    for ultag in soup.find_all('div', {'class': 'pull-right'}):
        pay_day_water_filter.append(ultag.text)

    bill_for_water = sum(result)

    pay_day = pay_day_water_filter[-1]

    pay_day = datetime.strptime(pay_day.strip(), "%d/%m/%Y")

    now = datetime.strptime(now, "%d.%m.%Y")

    time = pay_day - now

    ret_list = ['Telasi',str(time)[:6], bill_for_water]

    return ret_list
