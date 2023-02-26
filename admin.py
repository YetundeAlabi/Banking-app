from staff import StaffDb
from log import Logger
import csv
import string
import random
import pandas as pd
def random_password():
    return "".join((random.choice(string.ascii_letters) for x in range(7)))

logger = Logger()
db = StaffDb()


class Admin():
    def __init__(self, username="admin", password="devadmin"):
        
        self.username = username
        self.password = password
        self.logged_in = False
        
    def login(self, username, password):
        if username == self.username and password== self.password:
            self.logged_in = True
            print("Successfully logged in")
            logger.log_activity("admin logged in successfully")

    def logout(self):
        self.logged_in = False
        print("successfully logged out")
        logger.log_activity("admin logged out successfully")


    def create_staff(self):
        if not self.logged_in:
            print("You need to be logged in to add staff.")
        db.add_staff()
        
        
    def view(self, filename):
        if self.logged_in:
            with open(filename, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    print(row)
        logger.log_activity(f"admin viewed {filename} ")
 

    def view_logs(self, filename="log.txt"):
        if self.logged_in:
            with open(filename, "r") as file:
                log = file.readlines()
                print(log)
        

    def suspend_staff(self, staff):
        if self.logged_in:
            staff.is_suspended = True
            df = pd.read_csv("staff.csv")
            idx = staff.staff_id - 1
            df.loc[idx, "Is_suspended"] = True
            df.to_csv("staff.csv", index=False)
        logger.log_activity(f"{staff.name} suspended by admin")
        

    def reactivate_staff(self, staff):
        if not self.logged_in:
            print("You need to be logged in to reactivate staff")

        staff.is_suspended = False
        df = pd.read_csv("staff.csv")
        idx = staff.staff_id - 1
        df.loc[idx, "Is_suspended"] = False
        df.to_csv("staff.csv", index=False)
        logger.log_activity(f"{staff.name} reactivated by admin")
        

    