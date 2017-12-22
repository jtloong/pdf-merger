from apscheduler.schedulers.blocking import BlockingScheduler
import sqlite3

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=3)
def scheduled_job():
    os.remove(database.db)
    conn = sqlite3.connect('database.db')
    print ("Opened database successfully")
    conn.execute('CREATE TABLE files (user TEXT, timeOfVisit TEXT, filename TEXT, file BLOB)')
    print ("Table created successfully")
    conn.close()

sched.start()
