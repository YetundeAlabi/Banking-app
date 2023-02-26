# from customer import Customer, CustomerDb
from staff import Staff, StaffDb
from admin import Admin
import csv


import pandas as pd
from random import randint
import os


staff_db = StaffDb()


def account_no():
        range_start = 10**9
        range_end = (10**10)-1
        return randint(range_start, range_end)

file_exists = os.path.isfile('customer_data.csv')
if not file_exists:
    with open('customer_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Balance', 'Account Number'])



class Account:
    def __init__(self, customer_id, name, account_number, balance=0):
        self.customer_id = customer_id
        self.name = name
        self.balance = balance
        self.account_number = account_number

    def withdraw(self, amount):
        if amount > self.balance:
            print('Insufficient balance!')
            return
        self.balance -= amount
        df = pd.read_csv("customer_data.csv")
        num = self.customer_id - 1
        df.loc[num, "Balance"] = self.balance
        df.to_csv("customer_data.csv", index=False)
        print('Withdrawal successful!\n')

    def deposit(self, amount):
        self.balance += amount
        df = pd.read_csv("customer_data.csv")
        print(self.customer_id)
        num = self.customer_id - 1
        df.loc[num, "Balance"] = self.balance
        print(self.balance)
        df.to_csv("customer_data.csv", index=False)
        print('Deposit successful!\n')

    def transfer(self, recipient, amount):
        if amount > self.balance:
            print('Insufficient balance!')
            return
        self.balance -= amount
        recipient.balance += amount
        df = pd.read_csv("customer_data.csv")
        sender_index = self.customer_id - 1
        receiver_index = recipient.customer_id - 1
        df.loc[sender_index, "Balance"] = self.balance
        df.loc[receiver_index, "Balance"] = recipient.balance
        df.to_csv("customer_data.csv", index=False)
        print('Transfer successful!\n')

    def check_balance(self):
        return f'Your current balance is {self.balance}'

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

    def run(self):
        # main loop
        while True:
            print("Login as:")
            print("1. Customer")
            print("2. Staff")
            print("3. Admin")
            print("0. Quit")
            menu = input("Enter your role: ")
            if menu == "1":
                while True:
                    print('1. Create Account')
                    print('2. Withdraw')
                    print('3. Deposit')
                    print('4. Transfer')
                    print('5. Check Balance')
                    print('6. Quit')
                    choice = input('Enter your choice: ')
                    if choice == '1':
                        self.create_account()
                    elif choice == '2':
                        customer_id = int(input('Enter customer ID: '))
                        customer = self.find_customer(customer_id)
                        if customer:
                            amount = float(input('Enter amount to withdraw: '))
                            customer.withdraw(amount)
                        else:
                            print('Customer not found!')
                    elif choice == '3':
                        customer_id = int(input('Enter customer ID: '))
                        customer = self.find_customer(customer_id)
                        if customer:
                            amount = float(input('Enter amount to deposit: '))
                            customer.deposit(amount)
                        else:
                            print('Customer not found!')
                    elif choice == '4':
                        sender_id = int(input('Enter sender ID: '))
                        sender = self.find_customer(sender_id)
                        if sender:
                            recipient_id = int(input('Enter recipient ID: '))
                            recipient = self.find_customer(recipient_id)
                            if recipient:
                                amount = float(input('Enter amount to transfer: '))
                                sender.transfer(recipient, amount)
                            else:
                                print('Recipient not found!')
                        else:
                            print('Sender not found!')

                    elif choice == '5':
                        customer_id = int(input('Enter customer ID: '))
                        customer = self.find_customer(customer_id)
                        if customer:
                            bal = customer.check_balance()
                            print(bal)

                    elif choice == '6':
                        print("Thank you for using Nimi's Bank!")
                        break
                    else:
                        print('Invalid choice')

            elif menu == "3":
                username = input("Enter admin username: ")
                password = input("Enter admin password: ")
                admin = Admin()
                admin.login(username, password)

                while True:
                    print("\nAdmin actions:")
                    print("1. View logs")
                    print("2. Create staff member")
                    print("3. View customers")
                    print("4. view staff members")
                    print("5. Suspend staff member")
                    print("6. Reactivate staff member")
                    print("0. Logout \n")

                    admin_choice = input("Enter your choice: ")
                    
                    if admin_choice == "1":
                        admin.view_logs()
                        
                    elif admin_choice == "2":
                        admin.create_staff()
                        print("Staff member created successfully.")
                        
                    elif admin_choice == "3":
                        print("Customers:")
                        admin.view("customer_data.csv")
                        
                    elif admin_choice == "4":
                        print("Staff members:")
                        admin.view("staff.csv")

                    elif admin_choice == "5":
                        staff_id = int(input("Enter ID of staff member to suspend: "))
                        staff = staff_db.find_staff(staff_id)
                        if staff is not None:
                            admin.suspend_staff(staff)
                            print(staff.is_suspended)
                            # bank.logs.append(f"{name} suspended by admin.")
                            print("Staff member suspended successfully.")
                        else:
                            print("Staff member not found.")
                            
                    elif admin_choice == "6":
                        staff_id = int(input("Enter ID of staff member to reactivate: "))
                        print(staff_db.staff)
                        staff = staff_db.find_staff(staff_id)
                        if staff is not None:
                            admin.reactivate_staff(staff)
                            # bank.logs.append(f"{name} reactivated by admin.")
                            print("Staff member reactivated successfully.")
                        else:
                            print("Staff member not found.")

                    elif admin_choice == "0":
                        admin.logout()
                        break
             
                    else:
                        print("Invalid choice.")
                # else:
                    # print("Incorrect password.")
                
            elif menu == "0":
                print("Thank you for using for Nimi's Bank!")
                break
        
            else:
                print("Invalid choice.")

print("\nWelcome to Nimi's Bank!")
bank = Bank()
bank.run()


# def print_menu():
#     print("=" * 30)
#     print("1. Register")
#     print("2. Deposit")
#     print("3. Withdraw")
#     print("4. Transfer")
#     print("5. Quit")
#     print("=" * 30)

