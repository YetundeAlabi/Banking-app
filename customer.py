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
    last_id = 0
    def __init__(self, first_name, last_name, pin, phone, account_number, acct_type, balance):
        Customer.last_id += 1
        self.id = Customer.last_id
        self.first_name = first_name
        self.last_name = last_name
        self.pin = pin
        self.phone = phone
        self.account_number = account_number
        self.balance = balance
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


    def transfer(self, recipient, amount):
        if self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            df = pd.read_csv("customer.csv", index_col="acct_number")
            df.loc[self.account_num, "balance"] = self.balance
            df.loc[recipient.account_num, "balance"] = recipient.balance
            df.to_csv("customer.csv", index=False)
            logger.log_activity(f" customer {self.first_name} transferred {amount:,.2f} to {recipient.first_name}")
            return self.balance
