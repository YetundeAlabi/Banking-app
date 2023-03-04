from random import randint
import csv
from log import Logger
import pandas as pd
import os
import string

logger = Logger()

def account_no():
        range_start = 10**9
        range_end = (10**10)-1
        return randint(range_start, range_end)


alphabet = list(string.ascii_letters)
digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def ceaser(word, direction, shift=7):
    ceaser_cipher = ""
    if direction == "backward":
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


file_exists = os.path.isfile('customer_data.csv')
if not file_exists:
    with open('customer_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Firstname', 'Lastname', 'Pin', 'Phone', 'Account_Number','Acct_Type', 'Balance' ])


class Customer:
    def __init__(self, customer_id, first_name, last_name, pin, phone, account_number, acct_type, balance=0):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.pin = pin
        self.phone = phone
        self.account_number = account_number 
        self.acct_type = acct_type
        self.balance = balance
        self.logged_in = False

    
    def withdraw(self, amount):
        bal = int(self.balance)
        if amount > bal:
            print('Insufficient balance!')
            return
        bal -= amount
        self.balance = bal
        df = pd.read_csv("customer_data.csv")
        num = self.customer_id - 1
        df.loc[num, "Balance"] = self.balance
        df.to_csv("customer_data.csv", index=False)
        logger.log_activity(f"{self.first_name} withdrew {amount} from account")
        print('Withdrawal successful!\n')

    def deposit(self, amount):
        bal = int(self.balance)
        bal += amount
        self.balance = bal

        df = pd.read_csv("customer_data.csv")
        print(self.customer_id)
        num = self.customer_id - 1
        df.loc[num, "Balance"] = self.balance
        print(self.balance)
        df.to_csv("customer_data.csv", index=False)
        print('Deposit successful!\n')

    def transfer(self, recipient, amount):
        sender_bal = int(self.balance)
        print(sender_bal)
        recipient_bal = int(recipient.balance)
        print(recipient_bal)
        if amount > sender_bal:
            print('Insufficient balance!')
            return
        sender_bal -= amount
        recipient_bal += amount
        self.balance = sender_bal
        recipient.balance = recipient_bal
        df = pd.read_csv("customer_data.csv")
        sender_index = self.customer_id - 1
        receiver_index = recipient.customer_id - 1
        df.loc[sender_index, "Balance"] = self.balance
        df.loc[receiver_index, "Balance"] = recipient.balance
        df.to_csv("customer_data.csv", index=False)
        logger.log_activity(f"customer {self.first_name} transferred {amount:,.2f} to {recipient.first_name}")
        print('Transfer successful!\n')

    def check_balance(self):
        logger.log_activity(f"customer {self.first_name} has current balance {self.balance}")
        print(f'Your current balance is {self.balance:,.2f}')
    
    def customer_details(self):
        print(f"Name: {self.first_name} {self.last_name}")
        print(f"Account_number: {self.account_number}")
        print(f"Account type: {self.acct_type}")
        print(f"ID: {self.customer_id}")
        print("NOTE: keep your ID in mind")

    def login(self, account_number, password):
        if self.account_number == account_number and self.pin == password:
            self.logged_in = True
            print("Login successful!")
            logger.log_activity(f"Customer {self.first_name} logged in successfully")
            return True
        else:
            print("incorrect username or password")
            return False

    def logout(self):
        self.logged_in = False
        logger.log_activity(f"Customer {self.first_name} logged out successfully")
        return "successfully logged out"



class CustomerDb:

    def __init__(self):
        # load customer data from CSV file
        self.df = pd.read_csv('customer_data.csv')
        self.customers = []
        # create Account objects for each customer
        for i, row in self.df.iterrows():
            customer = Customer(row['ID'], row['Firstname'], row['Lastname'], row['Pin'], row['Phone'], row['Account_Number'], row['Acct_Type'], row['Balance'])
            self.customers.append(customer)

    def create_account(self):
        # get customer details
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        pin = input("Enter password: ")
        phone = input("Enter phone number: ")
        acct_type = input("Enter account_type: ")
        balance = 0
        # generate customer ID
        customer_id = len(self.customers) + 1
        account_number = account_no()
        # create new Account object for customer
        customer = Customer(customer_id, first_name=first_name, last_name=last_name, pin=ceaser(pin, direction="encrypt"), 
                            phone=phone, account_number=account_number, balance=balance, acct_type=acct_type)
        # append new customer to customers list
        self.customers.append(customer)
        # add new row to dataframe
        new_row = {'ID': customer_id, 'Firstname': first_name, 'Lastname': last_name, 'Pin': pin, 'Phone': phone,
                    'Account_Number': account_number, 'Acct_Type': acct_type, 'Balance': balance}
        self.df = self.df.append(new_row, ignore_index=True)
        # save updated dataframe to CSV file
        self.df.to_csv('customer_data.csv', index=False)
        logger.log_activity(f"A new customer {customer.first_name} account was created")
        print('Account created successfully!\n')
        customer.customer_details()
        print("\n")

    def find_customer(self, account_number):
        df = pd.read_csv("customer_data.csv")
        if len(self.customers) < len(df):
            df = pd.read_csv("customer_data.csv")

            for i, row in self.df.iterrows():
                customer = Customer(row['ID'], row['Firstname'], row['Lastname'], row['Pin'], row['Phone'], row['Account_Number'], row['Acct_Type'], row['Balance'])
                self.customers.append(customer)
        print(self.customers)
        for customer in self.customers:
            print(customer.account_number)
            print(type(customer.account_number))
            if customer.account_number == account_number:
                # print(type(customer.customer.id))
                return customer
        return None





























# from random import randint
# import csv
# from log import Logger
# import pandas as pd
# import os

# logger = Logger()

# def account_no():
#         range_start = 10**9
#         range_end = (10**10)-1
#         return randint(range_start, range_end)

# class Customer():
#     last_id = 0
#     def __init__(self, first_name, last_name, pin, phone, account_number, acct_type, balance):
#         Customer.last_id += 1
#         self.id = Customer.last_id
#         self.first_name = first_name
#         self.last_name = last_name
#         self.pin = pin
#         self.phone = phone
#         self.account_number = account_number
#         self.balance = balance
#         self.acct_type = acct_type

#         logger.log_activity(f"A new customer {self.first_name} account was created")

#     def get_balance(self):
#         logger.log_activity(f"{self.first_name} checked account balance")
#         return self.balance
    
    
#     def withdraw(self, amount):
#         if self.balance > amount:
#             print(self.balance)
#             self.balance -= amount
#             df = pd.read_csv("customer.csv", index_col="acct_number")
#             df.loc[self.account_num, "balance"] = self.balance
#             df.to_csv("customer.csv", index=False)
#             logger.log_activity(f"{self.first_name} withdrew {amount} from account")
#             print("Transaction successful")
#             return self.balance
#         else:
#             print("Insufficient balance")
        
#     def deposit(self, amount):
#         self.balance += amount
#         df = pd.read_csv("customer.csv", index_col="acct_number")
#         df.loc[self.account_num, "balance"] = self.balance
#         df.to_csv("customer.csv", index=False)
#         return self.balance


#     def transfer(self, recipient, amount):
#         if self.balance >= amount:
#             self.balance -= amount
#             recipient.balance += amount
#             df = pd.read_csv("customer.csv", index_col="acct_number")
#             df.loc[self.account_num, "balance"] = self.balance
#             df.loc[recipient.account_num, "balance"] = recipient.balance
#             df.to_csv("customer.csv", index=False)
#             logger.log_activity(f" customer {self.first_name} transferred {amount:,.2f} to {recipient.first_name}")
#             return self.balance
