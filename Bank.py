class Bank:
    def __init__(self):
        self.users = []
        self.total_balance = 0
        self.total_loan_amount = 0
        self.loan_feature_enabled = True
        self.next_account_number = 101  

    def create_account(self, name, email, address, account_type):
        account_number = self.next_account_number
        self.next_account_number += 1  
        user = User(name, account_number, email, address, account_type, self)
        self.users.append(user)
        return user

    def delete_account(self, user):
        if user in self.users:
            self.users.remove(user)
            print(f"Account {user.name} deleted successfully.")
        else:
            print("User not found.")

    def view_all_accounts(self):
        if not self.users:
            print("No accounts found.")
        else:
            for user in self.users:
                user.show_info()

    def check_total_balance(self):
        print(f"Total Available Balance: {self.total_balance} TK.")

    def check_total_loan_amount(self):
        print(f"Total Loan Amount: {self.total_loan_amount} TK.")

    def loan_feature(self):
        self.loan_feature_enabled = not self.loan_feature_enabled
        status = "enabled" if self.loan_feature_enabled else "disabled"
        print(f"Loan feature is now {status}.")

    def find_user(self, account_number):
        for user in self.users:
            if user.account_number == account_number:
                return user
        return None


class User:
    def __init__(self, name, account_number, email, address, account_type, bank):
        self.name = name
        self.account_number = account_number
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.bank = bank
        self.transaction_history = []
        self.loan_taken = 0

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.bank.total_balance += amount
            self.transaction_history.append(f"Deposited {amount} TK.")
        else:
            print("Invalid Amount")

    def withdraw(self, amount):
        if amount >= 0 and amount <= self.balance:
            self.balance -= amount
            self.bank.total_balance -= amount
            self.transaction_history.append(f"Withdrew {amount} TK.")
        elif amount < 0 or amount > self.balance:
            print("Withdrawal amount exceeded.")
        else:
            print("The Bank is bankrupt.")

    def show_info(self):
        print(f"\nInfo's of account {self.name}")
        print(f"Account Number: {self.account_number}")
        print(f"Account Type: {self.account_type}")
        print(f"Balance: {self.balance} TK.")

    def check_balance(self):
        print(f"Available Balance: {self.balance} TK.")

    def check_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)

    def take_loan(self, amount):
        if self.loan_taken < 2:
            self.balance += amount
            self.bank.total_loan_amount += amount
            self.transaction_history.append(f"Loan Taken: {amount} TK.")
            self.loan_taken += 1
            print(f"Loan of {amount} TK. taken successfully.")
        else:
            print("Unsuccessful because you have already taken the maximum number of loans and the maximum number of loans is 2 times.")

    def transfer(self, amount, target_account):
        target_account = int(target_account)  
        target_user = self.bank.find_user(target_account)
        if target_user is not None:
            if self.balance >= amount:
                self.balance -= amount
                target_user.balance += amount
                self.transaction_history.append(f"Transferred {amount} TK. to the Account Number: {target_account}")
                target_user.transaction_history.append(f"Received {amount} TK. from the Account Number: {self.account_number}")
                print(f"Amount {amount} TK. transferred to Account Number: {target_account} successfully.")
            else:
                print("Insufficient balance for the transfer.")
        else:
            print(f"Account {target_account} does not exist.")


class Admin(Bank):
    def __init__(self):
        super().__init__()

    def create_account(self, name, email, address, account_type):
        user = super().create_account(name, email, address, account_type)
        print(f"User account created successfully. Account number: {user.account_number}")

    def delete_account(self, target_account):
        try:
            target_account = int(target_account)
        except ValueError:
            print("Invalid account number. Please enter a valid account number.")
            return

        user = self.find_user(target_account)
        if user:
            self.users.remove(user) 
            print(f"Account Number: {target_account} deleted successfully.")
        else:
            print(f"Account Number: {target_account} is not found.")

    def view_all_accounts(self):
        super().view_all_accounts()

    def check_total_balance(self):
        super().check_total_balance()

    def check_total_loan_amount(self):
        super().check_total_loan_amount()

    def loan_feature(self):
        super().loan_feature()


admin = Admin()

while True:
    print("\nWelcome to the Banking Management System. Here are the options. Please select your suitable option.")
    print("If already you have an account choose option 1 else choose option 2 for creating the account with help of Admin Section\n")
    print("1. User Menu")
    print("2. Admin Menu")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        current_user = None
        while True:
            print("\nUser Menu:")
            print("1. Login")
            print("2. Exit")
            user_choice = input("Enter your choice: ")

            if user_choice == '1':
                account_number = int(input("Enter your Account Number: ")) 
                user = admin.find_user(account_number)
                if user:
                    current_user = user
                    break
                else:
                    print("User not found.")

            elif user_choice == '2':
                break

            else:
                print("Invalid choice. Choose 1 or 2.")

        if current_user is not None:
            while True:
                print(f'\nWelcome {current_user.name}\n')
                print('1. Show Info')
                print('2. Deposit')
                print('3. Withdraw')
                print('4. Check Balance')
                print('5. Check Transaction History')
                print('6. Take Loan')
                print('7. Transfer Money')
                print('8. Logout')
                user_option = input('Choose Option: ')

                if user_option == '1':
                    current_user.show_info()
                elif user_option == '2':
                    amount = float(input('Amount: '))
                    current_user.deposit(amount)
                elif user_option == '3':
                    amount = float(input('Amount: '))
                    current_user.withdraw(amount)
                elif user_option == '4':
                    current_user.check_balance()
                elif user_option == '5':
                    current_user.check_transaction_history()
                elif user_option == '6':
                    amount = float(input('Loan Amount: '))
                    current_user.take_loan(amount)
                elif user_option == '7':
                    target_account = input('Target Account Number: ')
                    amount = float(input('Transfer Amount: '))
                    current_user.transfer(amount, target_account)
                elif user_option == '8':
                    current_user = None
                    break
                else:
                    print('Invalid choice. Choose between 1 to 8.')

    elif choice == '2':
        while True:
            print("\nAdmin Menu:")
            print("1. Create Account")
            print("2. Delete Account")
            print("3. View All Accounts")
            print("4. Check Total Balance")
            print("5. Check Total Loan Amount")
            print("6. Loan Feature")
            print("7. Logout")
            admin_choice = input("Enter your choice: ")

            if admin_choice == '1':
                name = input("Name: ")
                email = input("Email: ")
                address = input("Address: ")
                account_type = input("Savings or Current? (Savings/Current): ")
                admin.create_account(name, email, address, account_type)

            elif admin_choice == '2':
                target_account = input('Target Account Number: ')
                admin.delete_account(target_account)

            elif admin_choice == '3':
                admin.view_all_accounts()

            elif admin_choice == '4':
                admin.check_total_balance()

            elif admin_choice == '5':
                admin.check_total_loan_amount()

            elif admin_choice == '6':
                admin.loan_feature()

            elif admin_choice == '7':
                break

            else:
                print("Invalid choice. Choose 1 to 7.")

    elif choice == '3':
        print("Thank You for using this service. Good Bye!")
        break

    else:
        print("Invalid choice. Choose 1, 2, or 3.")
