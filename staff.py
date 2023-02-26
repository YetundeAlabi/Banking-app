import csv
import string
import random
from log import Logger
from customer import Customer
import os
import pandas as pd

def random_password():
    return "".join((random.choice(string.ascii_letters) for x in range(10)))

logger = Logger()

staff_file = os.path.isfile('staff.csv')
if not staff_file:
    with open('staff.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Password', 'Is_suspended'])


class Staff:
    def __init__(self, staff_id, name, temp_password):
        self.staff_id = staff_id
        self.name = name
        self.temp_password = temp_password
        self.logged_in = False
        self.suspended = []
        self.is_suspended = False
        

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
        df = pd.read_csv("staff.csv")
        idx = self.staff_id - 1
        df.loc[idx, "Password"] = new_password
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
            bal = customer.check_balance()
            logger.log_activity(f"{self.name} checked customer{customer.first_name} balance")
            return f"{bal} Balance for {customer.first_name}"
            
    def display_staff_details(self):
        details = f"name : {self.name}, password: {self.temp_password}, is_suspended: {self.is_suspended}"
        return details
    



class StaffDb:

    def __init__(self):
        self.df = pd.read_csv("staff.csv")
        self.staff = []

        for i, row in self.df.iterrows():
            staff = Staff(row['ID'], row['Name'], row['Password'])
            self.staff.append(staff)

    def add_staff(self):
        name = input('Enter staff member name: ')
        temp_password = random_password()
        staff_id = len(self.staff) + 1
        staff = Staff(staff_id, name, temp_password)
        self.staff.append(staff)

        new_row = {'ID': staff_id, 'Name': name, 'Password': temp_password, 'Is_suspended': staff.is_suspended}
        self.df = self.df.append(new_row, ignore_index=True)
        # save updated dataframe to CSV file
        self.df.to_csv('staff.csv', index=False)
        print('Staff created successfully!\n')


    def find_staff(self, staff_id):
        print(self.staff)
        for staff in self.staff:
            print(staff.staff_id)
            if staff.staff_id == staff_id:
                return staff
        return None

            
    
