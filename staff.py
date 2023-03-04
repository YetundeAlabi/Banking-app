import csv
import string
import random
from log import Logger
from customer import Customer
import os
import pandas as pd


alphabet = list(string.ascii_letters)
digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def random_password():
    return "".join((random.choice(string.ascii_letters) for x in range(10)))


def ceaser(word, direction, shift=7):
    ceaser_cipher = ""
    if direction == "decrypt":
        shift *= -1
    for char in word:
        if char.isdigit():
            index = digits.index(int(char)) + shift
            index = index % len(digits)
            char = str(digits[index])
        elif char in alphabet:      
            index = (alphabet.index(char) + shift) % len(alphabet)
            if char.isupper():
                char = alphabet[index].lower() 
            elif char.islower():
                char = alphabet[index].upper()
        ceaser_cipher += char
   
    return ceaser_cipher


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
        self.is_suspended = False
        
        
    def first_login(self, username, password):
        if self.name == username and self.temp_password == password:
            self.logged_in = True
            print("Login for first time successful!")
            logger.log_activity(f"staff {self.name} logged in successfully for the first time")

        
    def login(self, username, password):
        if self.name == username and self.temp_password == ceaser(password, direction="encrypt") and self.is_suspended == False:
            self.logged_in = True
            print("Login successfully!")
            logger.log_activity(f"staff {self.name} logged in successfully")
            return True
        else:
            print("incorrect username or password")
            return False

    def logout(self):
        self.logged_in = False
        logger.log_activity(f"staff {self.name} logged out successfully")
        return "successfully logged out"

    def change_password(self, new_password):
        df = pd.read_csv("staff.csv")
        idx = self.staff_id - 1
        df.loc[idx, "Password"] = ceaser(new_password,"encrypt")
        df.to_csv("staff.csv", index=False)
        logger.log_activity(f"staff {self.name} changed password")
        return self.display_staff_details()


    def deposit(self, customer, amount):
        if self.logged_in:
            customer.deposit(amount)
            logger.log_activity(f"Deposit of {amount} successfully made for customer {customer.first_name} by {self.name}")
            print(f"Deposit of {amount:,.2f} successfully made for customer {customer.first_name}")

        else:
            return "You must be logged in to make a deposit."


    def view_bal(self, customer):
        if self.logged_in:
            customer.check_balance()
            logger.log_activity(f"{self.name} checked customer {customer.first_name} balance")
            # return f"{bal} Balance for {customer.first_name}"
            
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
        logger.log_activity(f"admin created a new staff {staff.name}")
        staff.display_staff_details()
        print('Staff created successfully!\n')


    def find_staff(self, staff_id):
        df = pd.read_csv("staff.csv")
        if len(self.staff) < len(df):
            df = pd.read_csv("staff.csv")

            for i, row in df.iterrows():
                staff = Staff(row['ID'], row['Name'], row['Password'])
                self.staff.append(staff)

        for staff in self.staff:
            # print(type(staff.staff_id))
            if staff.staff_id == staff_id:
                return staff
        return None
        


 
