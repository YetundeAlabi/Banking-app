from customer import Customer
import pandas as pd

class Bank:
    def __init__(self):
        # load customer data from CSV file
        self.df = pd.read_csv('customer_data.csv')
        self.customers = []
        # create Account objects for each customer
        for i, row in self.df.iterrows():
            customer = Account(row['ID'], row['Name'], row['Account Number'], row['Balance'])
            self.customers.append(customer)

    def create_account(self):
        # get customer details
        name = input('Enter your name: ')
        balance = 0
        # generate customer ID
        customer_id = len(self.customers) + 1
        account_number = account_no()
        # create new Account object for customer
        customer = Account(customer_id, name, account_number=account_number, balance=balance)
        # append new customer to customers list
        self.customers.append(customer)
        # add new row to dataframe
        new_row = {'ID': customer_id, 'Name': name, 'Account Number': account_number, 'Balance': balance}
        self.df = self.df.append(new_row, ignore_index=True)
        # save updated dataframe to CSV file
        self.df.to_csv('customer_data.csv', index=False)
        print('Account created successfully!\n')

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None
