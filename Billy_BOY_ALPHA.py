from datetime import datetime
from bs4 import BeautifulSoup
import requests
from urllib import parse
import json
import time


################################## MAIN CODE ###############################################

########### USERAREA.MAGTI.GE #####

# Change Values *required:

#CO/MAGTI
Username = 'YOUR CO/MAGTI USERNAME'
Password = 'YOUR CO/MAGTI PASSWORD'
###

#Telasi
Telasi_id = 'ID'

###########################

session = requests.Session()
session.cookies.get_dict()

frst_post = session.post("https://userarea.magticom.ge", data={'UserName': Username, 'Password': Password})

frst_view = BeautifulSoup(frst_post.text,'lxml')

attrs = {}
for vals in frst_view.findAll('input'):
    attrs[vals['id'][3:]] = vals['value']

attrs['TabIndex'] = '0'

headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.8,ru;q=0.6,ka;q=0.4',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Length':'84',
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'__utma=142200110.405086356.1478026025.1478467079.1481496629.3; _ga=GA1.2.405086356.1478026025; '
             'ASP.NET_SessionId=%(ASP.NET_SessionId)s'% session.cookies.get_dict(),
    'Host':'userarea.magticom.ge',
    'Origin':'https://userarea.magticom.ge',
    'Pragma':'no-cache',
    'Referer':'%s' % frst_post.url,
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
}

scnd_post = requests.post('https://userarea.magticom.ge/Services/LoadTab', data=parse.urlencode(attrs).encode(),headers=headers)

scnd_view = BeautifulSoup(scnd_post.text,'html.parser')

eaten = json.loads(scnd_view.text)


third_view = BeautifulSoup(eaten['Data'],'html.parser')

dirty_p = third_view.findAll('p')
clean_p = []

for clean in dirty_p:
    clean_p.append(clean.text)

latest_dict = dict([(k, v) for k,v in zip (clean_p[::2], clean_p[1::2])])

time.strftime("%d/%m/%Y")

pay_day = latest_dict['გათიშვის თარიღი']

pay_day = datetime.strptime(pay_day, "%d.%m.%Y")

now = time.strftime("%d.%m.%Y")

now = datetime.strptime(now, "%d.%m.%Y")

time = pay_day - now

print (time,'left\n',"ბალანსი:",latest_dict['ბალანსი']+(' ლ'))
########### MAGTI FINISHED######

########### TELASI #######
frst_post = requests.get('http://my.telasi.ge/customers/info/%s' % Telasi_id)
soup = BeautifulSoup(frst_post.text,'html.parser')
for code in soup.findAll('code'):
    print(code.text)

for i in soup.find_all_next("i", { "class" : "fa fa-time" }):
    print(i.value)

pay_day_water_filter = []
for ultag in soup.find_all('div', {'class': 'pull-right'}):
    pay_day_water_filter.append(ultag.text)

pay_day_water = pay_day_water_filter[-1]


print(pay_day_water)