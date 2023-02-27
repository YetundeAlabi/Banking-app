import csv
import datetime
import  os

class Logger:
    def __init__(self):
        self.filename = 'log.txt'
        log_file = os.path.isfile(self.filename)

        if not log_file:
            with open(self.filename, mode='w') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Time', 'Activity'])

    def log_activity(self, activity):
        current_time = datetime.datetime.now()
        with open(self.filename, mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([current_time.date(), current_time.time(), activity])
