from customer import CustomerDb
from staff import StaffDb
from admin import Admin
from log import Logger

staff_db = StaffDb()
customer_db = CustomerDb()
logger = Logger()

class Bank:
    
    def run(self):
        # main loop
        while True:
            print("Login as:")
            print("1. Customer")
            print("2. Staff")
            print("3. Admin")
            print("0. Quit\n")

            menu = input("Enter your role: ")
            if menu == "1":
                print("=" * 30)
                print('1. Create Account')
                print('2. Perform other transactions')
                print("=" * 30)
                print("\n")
                cust_option = input("Enter an option: ")
                if cust_option == "1":
                    customer_db.create_account()

                elif cust_option == "2":
                    print("Welcome!!!\n")
                    customer_acc = int(input("Enter your account number: "))
                    password = input("Enter your password: ") 
                    customer = customer_db.find_customer(customer_acc)
                    login = customer.login(customer_acc, password)
                    if login:
                        while True:
                            print("=" * 30)
                            print('1. Withdraw')
                            print('2. Deposit')
                            print('3. Transfer')
                            print('4. Check Balance')
                            print('5. Quit\n')
                            print("=" * 30)

                            choice = input('Enter your choice: ')
                            
                            if choice == '1':
                                amount = float(input('Enter amount to withdraw: '))
                                customer.withdraw(amount)
                            
                            elif choice == "2":
                                amount = float(input('Enter amount to deposit: '))
                                customer.deposit(amount)
                                
                            elif choice == '3':
                                recipient_acc = int(input('Enter recipient account number: '))
                                recipient = customer_db.find_customer(recipient_acc)
                                if recipient:
                                    amount = float(input('Enter amount to transfer: '))
                                    customer.transfer(recipient, amount)
                                else:
                                    print('Receipient not found!')

                            elif choice == '4':
                                customer.check_balance()


                            elif choice == '5':
                                print("Thank you for using Nimi's Bank!")
                                break
                            else:
                                print('Invalid choice')
                    

                else:
                    print('Customer not found!')


            elif menu == "2":
                username = input("Enter staff username: ")
                staff = staff_db.find_staff(username)
                if staff is not None:
                    first = input("If this is your first time login in \nPress Y for Yes, N if No: ")   
                    if first == "Y":
                        password = input("Enter temp password: ")
                        staff.first_login(username, password)
                        new_password = input("Enter new password: ")
                        staff.change_password(new_password)
                    else:
                        password = input("Enter password: ")
                        login = staff.login(username, password)
                        if login: 
                            if staff.is_suspended == True:
                                print(f"{staff.name} has being suspended. Contact the admin for reactivation")
                                logger.log_activity(f'{staff.name} tried to login on the suspended account')
                                break
                        else:
                            break
    
                    while True:
                        print("\nStaff actions:")
                        print("1. Deposit for customer")
                        print("2. View customer balance")
                        print("3. Logout\n")

                        staff_choice = input("Enter your choice: ")

                        if staff_choice == "1":
                            customer_acc = int(input("Enter your account number: "))
                            customer = customer_db.find_customer(customer_acc)
                            if customer:
                                amount = float(input('Enter amount to deposit: '))
                                staff.deposit(customer, amount)
                            else:
                                print("Customer not found")

                        elif staff_choice == "2":
                            customer_acc = int(input("Enter your account number: "))
                            customer = customer_db.find_customer(customer_acc)
                            if customer:
                                staff.view_bal(customer)

                        elif staff_choice == "3":
                            staff.logout()
                            break

                        else:
                            print("Invalid choice")

                        
                else:
                    print("Staff not found")
                

            elif menu == "3":
                username = input("Enter admin username: ")
                password = input("Enter admin password: ")
                admin = Admin()
                login = admin.login(username, password)
                if not login:
                    print("Incorrect crendentials.")
                    break
                    
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
                        staff_name = input("Enter name of staff member to suspend: ")
                        staff = admin.staff_db(staff_name)
                        if staff is not None:
                            admin.suspend_staff(staff)
                            
                            # bank.logs.append(f"{name} suspended by admin.")
                            print(f"Staff member suspended successfully.")
                        else:
                            print("Staff member not found.")
                            
                    elif admin_choice == "6":
                        staff_name = input("Enter name of staff member to reactivate: ")
                        staff = admin.staff_db(staff_name)
                        if staff is not None:
                            admin.reactivate_staff(staff)
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


