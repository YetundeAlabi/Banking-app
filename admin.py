from staff import Staff, StaffDb
from log import Logger
import csv
import string
import random
def random_password():
    return "".join((random.choice(string.ascii_letters) for x in range(7)))

logger = Logger()
db = StaffDb()

class Admin():
    def __init__(self, username="admin", password="devadmin"):
        # super().__init__(name, temp_password)
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


    def create_staff(self, name, temp_password=random_password()):
        if not self.logged_in:
            print("You need to be logged in to add staff.")

        new_staff = Staff(name, temp_password)
        # print("New Staff Added:")
        # new_staff.display_staff_details()
        db.add_staff(new_staff)
        db.save_to_csv()
        logger.log_activity(f"admin created a new staff {new_staff.name}")

        
    def view(self, filename):
        if self.logged_in:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    print(row)
 

    def view_logs(self, filename = "log.txt"):
        if self.logged_in:
            with open(filename, "r") as file:
                log = file.readlines()
                print(log)
        

    def suspend_staff():
        # staff.is_suspended = True
        pass

    def reactivate_staff():
        # staff.is_supended
        pass


