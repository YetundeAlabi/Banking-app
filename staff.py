import csv
import string
import random
from log import Logger
from customer import Customer
import os
import pandas as pd

# def random_password():
#     return "".join((random.choice(string.ascii_letters) for x in range(7)))

logger = Logger()
class Staff():
    def __init__(self, name, temp_password,):
        self.name = name
        self.temp_password = temp_password
        self.logged_in = False
        self.suspended = []
        self.is_suspended = False
        
        # with open(self.filename, mode='a') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([self.name, self.temp_password])

    def login(self, username, password):
        if self.name == username and self.temp_password == password:
            self.logged_in = True
            print("Login successfully!")
            logger.log_activity("staff logged in successfully")

        else:
            print("incorrect username or password")

    def logout(self):
        self.logged_in = True
        logger.log_activity("staff logged out successfully")
        return "successfully logged out"

    def change_password(self, new_password):
        df = pd.read_csv("staff.csv", index_col="name")
        df.loc[self.name, "temp_password"] = new_password
        df.to_csv("staff.csv", index=False)
        logger.log_activity(f"staff {self.name} changed password")
        return self.display_staff_details()


    def deposit(self, customer:Customer, amount):
        if self.logged_in:
            customer.deposit(amount)
            logger.log_activity(f"Deposit of {amount} successfully made for customer {customer.first_name} by {self.name}")
            return f"Deposit of {amount} successfully made for customer{customer.first_name}"

        else:
            return "You must be logged in to make a deposit."


    def view_bal(self, customer:Customer):
        if self.logged_in:
            bal = customer.get_balance()
            logger.log_activity(f"{self.name} checked customer{customer.name} balance")
            return f"{bal} Balance for {customer.name}"
            
    def display_staff_details(self):
        details = f"name : {self.name}, password: {self.temp_password}, is_suspended: {self.is_suspended}"
        return details
    
        

class StaffDb:

    def __init__(self, filename="staff.csv"):
         self.filename = filename
         self.staff = []

    def add_staff(self, staff):
         self.staff.append(staff)
         return self.staff
    
    def save_to_csv(self):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, "a", newline="") as file:
            headers = ["username", "password", "is_suspended"]
            writer = csv.DictWriter(file, delimiter=',', lineterminator='\n',fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            else:
                for staff in self.staff:
                    writer.writerow([staff.name, staff.temp_password, staff.is_suspended])
 
