# Password Manager Menus
# Author: Yingyi Liao
# For private use only

finish = False
login_successful = False

def login_menu():
    print('Welcome to use Password Manager')
    print('1. Login')
    print('2. Register')
    print('3. Exit')
    while True:
        choice = str(input('Please enter your choice:'))
        if choice == '1':
            login()
            break
        elif choice == '2':
            register()
            break
        elif choice == '3':
            exit_with2sdelay()
            break
        else:
            print('Invalid input. Please try again!')


def function_menu():
    print(f'You have been login as {loginAcc}')
    print('1. Create new username and password')
    print('2. Query')
    print('3. Exit')
    while True:
        choice = str(input('Please enter your choice:'))
        if choice == '1':
            saving_new_entry()
            break
        elif choice == '2':
            query_maneu()
            break
        elif choice == '3':
            exit_with2sdelay()
            break
        else:
            print('Invalid input. Please try again!')


def query_menu():
    print('Please choose your query type!')
    print('1. Query from source')
    print('2. Query from account user name')
    print('3. Query from date')
    print('4. Exit')
    while True:
        choice = str(input('Please enter your choice:'))
        if choice == '1':
            query_from_source()
            break
        elif choice == '2':
            query_from_acc_name()
            break
        elif choice == '3':
            query_from_date()
            break
        elif choice == '4':
            exit_with2sdelay()
            break
        else:
            print('Invalid input. Please try again!')


while not finish:
    if not login_successful:
        login_menu()
    else:
        function_menu()