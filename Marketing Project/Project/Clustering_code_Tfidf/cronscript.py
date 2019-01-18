from crontab import CronTab
from datetime import datetime

cron = CronTab(user='ubuntu')

cron.remove_all()  

job = cron.new(command='/home/ubuntu/anaconda3/bin/python /home/ubuntu/Python/Generalize8.py', comment='comment')  
job.minute.every(30)

for item in cron:  
    print(item)

print(job.is_enabled())
myFile = open('append.txt', 'a')  
myFile.write('\nAccessed on ' + str(datetime.now())) 

cron.write()  
