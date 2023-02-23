from customer import Customer, CustomerDb
from staff import Staff
from admin import Admin, StaffDb
import csv
# db = CustomerDb()
# staff_db = StaffDb()
# admin = Admin("nimi","1234","nimi", "nimi@0123")
# admin.login("nimi", "nimi@0123")
# admin.create_staff("fola")
# admin.create_staff("Toluwanimi")
# admin.create_staff("Tola")
# admin.create_staff("sola")
# admin.view("customer.csv")

# tola = Staff("tola", "1234")
# tola.login("tola", "1234")

# customer1 = Customer(first_name="Yetunde", last_name="Alabi", pin="nimi@0123", acct_type="saving", phone="081234587")
# customer2 = Customer(first_name="Bobo", last_name="Alabi", pin="bob@0123", acct_type="saving", phone="081234587")
# db.add_customer(customer1)
# db.add_customer(customer2)
# db.add_to_csv()
# tola.deposit(customer1, 2000)
# customer1.withdraw(50)
# # logger.log_activity("added customer to db")
customer1 = Customer(first_name="Nimi", last_name="Alabi", pin="nimi@0123", acct_type="saving", phone="081234587")
nimi = Admin()
nimi.login("admin", "devadmin")
nimi.create_staff("Toluwani")

# customer login
# name = input("Enter username: ")
# password = input("Enter password: ")
# with open("staff.csv", "r") as file:
#     reader = csv.reader(file)
#     for row in reader:
#         username = row[0]
#         pin = row[1]
#         if name == username and password == pin:
#             name = Staff(name=name, temp_password=password)
#             name.login(username=name, password=password)

        # print(row)



