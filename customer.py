from random import randint
import csv
from log import Logger
import pandas as pd
import os

logger = Logger()

def account_no():
        range_start = 10**9
        range_end = (10**10)-1
        return randint(range_start, range_end)

class Customer():
    def __init__(self, first_name, last_name, pin, acct_type,phone):
        self.first_name = first_name
        self.last_name = last_name
        self.pin = pin
        self.phone = phone
        self.account_num = account_no()
        self.balance = 0
        self.acct_type = acct_type

        logger.log_activity(f"A new customer {self.first_name} account was created")

    def get_balance(self):
        logger.log_activity(f"{self.first_name} checked account balance")
        return self.balance
    
    
    def withdraw(self, amount):
        if self.balance > amount:
            print(self.balance)
            self.balance -= amount
            df = pd.read_csv("customer.csv", index_col="acct_number")
            df.loc[self.account_num, "balance"] = self.balance
            df.to_csv("customer.csv", index=False)
            logger.log_activity(f"{self.first_name} withdrew {amount} from account")
            print("Transaction successful")
            return self.balance
        else:
            print("Insufficient balance")
        
    def deposit(self, amount):
        self.balance += amount
        df = pd.read_csv("customer.csv", index_col="acct_number")
        df.loc[self.account_num, "balance"] = self.balance
        df.to_csv("customer.csv", index=False)
        return self.balance


class CustomerDb:

    def __init__(self, filename="customer.csv"):
         self.filename = filename
         self.customers = []

    def add_customer(self, customer):
         self.customers.append(customer)
         return self.customers
    
    def add_to_csv(self):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, "a", newline="") as file:
            headers = ["first_name", "last_name", "pin", "phone", "acct_number", "balance", "acct_type" ]
            writer = csv.DictWriter(file, delimiter=',', lineterminator='\n',fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            else:
                for customer in self.customers:
                    writer.writerow([customer.first_name, customer.last_name, customer.pin, customer.phone, customer.account_num,
                                        customer.balance, customer.acct_type])
            