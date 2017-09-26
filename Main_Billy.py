import os
import time
import random
import magti
import telasi


# Change Values *required:

#CO/MAGTI
Username = 'YOUR CO/MAGTI USERNAME'
Password = 'YOUR CO/MAGTI PASSWORD'
###

#Telasi
Telasi_id = 'ID'


# Notify me to pay


until_its_left = 3  # days

now = time.strftime("%d.%m.%Y")

# running external py functions

print('telasi = ',telasi.telasi_bil(Telasi_id, now))

print('magti = ',magti.magti_bil(Username,Password,now))


# end of running them

def notifications(From,Message):
    os.system('notify-send "%s" "%s"' % (From, Message))

notifications(telasi.telasi_bil(Telasi_id, now)[0],telasi.telasi_bil(Telasi_id, now)[1]+' left\n'
              +str(telasi.telasi_bil(Telasi_id, now)[2])+' ლარი')

notifications(magti.magti_bil(Username,Password,now)[0],magti.magti_bil(Username,Password,now)[1]+' left\n'
              +str(magti.magti_bil(Username,Password,now)[2]) +' ლარი')


while True:

    if int(telasi.telasi_bil(Telasi_id, now)[1][:2]) <= until_its_left or int(magti.magti_bil(Username,Password,now)[1][:2]) <= until_its_left:

        os.system("gnome-terminal -e 'python ./payment.py'")

        break

    else:

        hr_in_sec = [10800, 7200] # 3 or 2

        notifications('Billy','I go sleep')

        time.sleep(random.choice(hr_in_sec))

