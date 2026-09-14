# Password Manager all parts combine
# Author: Yingyi Liao
# For private use only

import clipboard
import datetime
import hashlib
import random
import stdiomask
import string
import threading
import pyodbc as odbc
from cryptography.fernet import Fernet
from prettytable import PrettyTable

# declare globals
login_successful = False
finish = False
global getLogin_ID
global loginAcc


# initial connection to local SQL server
# DRIVER_NAME, SERVER_NAME, DATABASE_NAME are subject to change for localisation
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'MIDDLETOHIGH'
DATABASE_NAME = 'PasswordManager'
connection_string = f"DRIVER={DRIVER_NAME};\n" \
                    f"SERVER={SERVER_NAME};\n" \
                    f"DATABASE={DATABASE_NAME};\n" \
                    f"Trust_Connection=yes;"

conn = odbc.connect(connection_string)
cursor = conn.cursor()


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
            exit_delay_2_second()
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
            query_menu()
            break
        elif choice == '3':
            exit_delay_2_second()
            break
        else:
            print('Invalid input. Please try again!')


def query_menu():
    print('Please choose your query type!')
    print('1. Query from source')
    print('2. Query from account user name')
    print('3. Query from date')
    print('4. Query from all')
    print('5. Exit')
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
            query_from_all()
            break
        elif choice == '5':
            exit_delay_2_second()
            break
        else:
            print('Invalid input. Please try again!')


def login():
    global login_successful, loginAcc, getLogin_ID
    while not login_successful:
        loginAcc = str(input('Please enter your login account:'))
        loginPwd = hashlib.sha256(stdiomask.getpass(prompt='Please enter your login password:', mask='*').encode()).hexdigest()
        # match hashed password in database
        query = f'SELECT COUNT(*) FROM Login WHERE (LoginAcc = \'{loginAcc}\' and LoginPwd = \'{loginPwd}\')'
        cursor.execute(query)
        for x in cursor:
            y = list(x)
            if y[0] == 1:
                login_successful = True
                # get login_ID from SQL for further reference
                print(f'Login successful, welcome {loginAcc}')
                query3 = f'SELECT Login_ID FROM Login WHERE (LoginAcc = \'{loginAcc}\')'
                cursor.execute(query3)
                for z in cursor:
                    getLogin_ID = z[0]
        else:
            print('Incorrect login account or password')


def new_account():
    while True:
        newAcc = str(input('Please enter your new login account:'))
        # eliminate blank
        if len(newAcc) == 0:
            print('New login account can not be blank!\nPlease try again!')
        # eliminate space and special characters
        elif newAcc != ''.join(_ for _ in newAcc if _.isalnum()):
            print('Account can not contain space or special characters!\nPlease try again!')
        # eliminate repeating account
        else:
            query = f'SELECT COUNT(*) FROM Login WHERE (LoginAcc = \'{newAcc}\')'
            cursor.execute(query)
            for x in cursor:
                y = list(x)
                if y[0] == 0:
                    return newAcc
                else:
                    print('Account exists.\nPlease try again!\n')


def new_password():
    while True:
        choice = str(input('Do you want to generate random password? Yes/No')).lower()
        if choice == 'yes':
            newPwd = generate_random_password()
            return newPwd
        elif choice == 'no':
            while True:
                newPwd = str(input('Please enter your new login password:'))
                # manual password only 1 rule = no blank password. anything else even white space is accepted
                if len(newPwd) == 0:
                    print('New login password can not be blank!\nPlease try again!')
                else:
                    return newPwd
        else:
            print('Invalid input!\nPlease try again!')


def register():
    newAcc = new_account()
    # hashing password and inserting account details in database
    newPwd = hashlib.sha256((new_password()).encode()).hexdigest()
    query = f'INSERT INTO Login (LoginAcc, LoginPwd) VALUES (\'{newAcc}\', \'{newPwd}\')'
    cursor.execute(query)
    conn.commit()
    print('New login created successful!')


def source():
    while True:
        # source name got to be something
        uSource = str(input('Please enter the source of new entry:'))
        if len(uSource) == 0 or len(uSource.strip(' ')) == 0:
            print('The source can not be blank or contains only white space!\nPlease try again!')
        else:
            break
    # if the source does not exist in the database, create a new one
    query = f'SELECT COUNT(*) FROM Source WHERE (SourceName = \'{uSource}\')'
    cursor.execute(query)
    for x in cursor:
        if x[0] > 0:
            return uSource
        else:
            insert_query = f'INSERT INTO Source (SourceName) VALUES (\'{uSource}\')'
            cursor.execute(insert_query)
            conn.commit()
            return uSource


def new_entry_id():
    while True:
        # not picky in naming id, but at least something
        uNewID = str(input('Please enter the new account of new entry:'))
        if len(uNewID) == 0 or len(uNewID.strip(' ')) == 0:
            print('The source can not be blank or contains only white space!\nPlease try again!')
        else:
            return uNewID


def copy_password(x):
    # copy function when creating new password
    copy_pwd = input('Do you want to copy the password to clipboard?:(Yes/anything else is no)').lower()
    if copy_pwd == 'yes':
        clipboard.copy(x)
        print('The password has been copied into clipboard!')


def new_entry_pwd():
    while True:
        choice = str(input('Do you want to generate random password? Yes/No')).lower()
        if choice == 'yes':
            uNewPwd = generate_random_password()
            copy_password(uNewPwd)
            return uNewPwd
        elif choice == 'no':
            # manual password is also not picky. only no empty.
            uNewPwd = str(input('Please enter the new password of new entry:'))
            if len(uNewPwd) == 0 or len(uNewPwd.strip(' ')) == 0:
                print('The source can not be blank or contains only white space!\nPlease try again!')
            else:
                copy_password(uNewPwd)
                return uNewPwd


def encrypt_new_entry_pwd():
    # pairing key and token from encryption
    encrypt = new_entry_pwd()
    key = Fernet.generate_key()
    f = Fernet(key)
    b = bytes(f'{encrypt}'.encode())
    token = f.encrypt(b)
    encrInfo = [key, token]
    return encrInfo


def saving_new_entry():
    uSource = source()
    newID = new_entry_id()
    pwdInfo = encrypt_new_entry_pwd()
    key, token = pwdInfo[0], pwdInfo[1].decode()
    comment = str(input('Please input comment:'))
    query2 = f'SELECT Source_ID FROM Source WHERE (SourceName = \'{uSource}\')'
    cursor.execute(query2)
    for y in cursor:
        getSource_ID = y[0]
    # inserting record with encrypted token
    query3 = (f'INSERT INTO Store (Login_ID, Source_ID, UserAcc, UserPwd, StoreComm, Time) '
              f'VALUES (\'{getLogin_ID}\', '
              f'\'{getSource_ID}\', '
              f'\'{newID}\', '
              f'\'{token}\', '
              f'\'{comment}\', '
              f'CURRENT_TIMESTAMP)')

    cursor.execute(query3)
    conn.commit()
    # taking Store_ID from database
    query4 = (f'SELECT Store_ID FROM Store '
              f'WHERE '
              f'(Login_ID = {getLogin_ID} and '
              f'Source_ID = {getSource_ID} and '
              f'UserACC= \'{newID}\' and '
              f'UserPwd = \'{token}\')')

    cursor.execute(query4)
    for z in cursor:
        getStore_ID = z[0]

    keyFile = f'{loginAcc}.key'
    with open(keyFile, 'a') as f:
        # use store ID as ID for encryption Key from divider in key file
        f.write(key.decode() + ':divider:' + str(getStore_ID) + '\n')

    print('New User Account created successful')


def query_from_source():
    while True:
        qSource = str(input('Please entry the query source:'))
        if len(qSource) == 0 or len(qSource.strip(' ')) == 0:
            print('Source can not be blank or contains while space only!\n Please try again')
        else:
            break

    query1 = f'SELECT COUNT(*) FROM Source WHERE (SourceName = \'{qSource}\')'
    cursor.execute(query1)
    for x in cursor:
        if x[0] == 0:
            print('This source does not exist!')
        else:
            query2 = f'SELECT Source_ID FROM Source WHERE (SourceName = \'{qSource}\')'
            cursor.execute(query2)
            for y in cursor:
                getSource_ID = y[0]

            query3 = f'SELECT COUNT(*) FROM Store WHERE (Login_ID = {getLogin_ID} and Source_ID = {getSource_ID})'
            cursor.execute(query3)
            for p in cursor:
                if p[0] == 0:
                    print('This source does not exist!')
                else:
                    query4 = (f'SELECT Store_ID, SourceName, UserAcc, UserPwd, StoreComm, Time '
                              f'FROM Store '
                              f'LEFT JOIN Login on Store.Login_ID = Login.Login_ID '
                              f'LEFT JOIN Source on Store.Source_ID = Source.Source_ID '
                              f'WHERE Store.Login_ID = {getLogin_ID} and Store.Source_ID = {getSource_ID}')
                    cursor.execute(query4)
                    decrypt_pwd()


def query_from_acc_name():
    while True:
        qAccName = str(input('Please entry the account user name:'))
        if len(qAccName) == 0 or len(qAccName.strip(' ')) == 0:
            print('Account user name can not be blank or contains while space only!\n Please try again')
        else:
            break

    query1 = f'SELECT COUNT(*) FROM Store WHERE (UserAcc = \'{qAccName}\' and Login_ID = {getLogin_ID})'
    cursor.execute(query1)
    for x in cursor:
        if x[0] == 0:
            print('This account user name does not exist!')
        else:
            query2 = (f'SELECT Store_ID, SourceName, UserAcc, UserPwd, StoreComm, Time '
                      f'FROM Store '
                      f'LEFT JOIN Login on Store.Login_ID = Login.Login_ID '
                      f'LEFT JOIN Source on Store.Source_ID = Source.Source_ID '
                      f'WHERE Store.Login_ID = {getLogin_ID} and Store.UserAcc = \'{qAccName}\'')
            cursor.execute(query2)
            decrypt_pwd()


def query_from_date():
    while True:
        qDate = str(input('Please entry the date entry created(YYYY-MM-DD):'))
        try:
            d = datetime.date.fromisoformat(qDate)
            e = d + datetime.timedelta(days=1)
            break
        except ValueError:
            print('Please enter in correct date format!')

    query1 = (f'SELECT COUNT(*) FROM Store '
              f'WHERE (Time >= \'{d} 00:00:00.000\' and '
              f'Time <= \'{e} 00:00:00.000\' and '
              f'Login_ID = {getLogin_ID})')
    cursor.execute(query1)
    for x in cursor:
        if x[0] == 0:
            print('This date does not exist!')
        else:
            query2 = (f'SELECT Store_ID, SourceName, UserAcc, UserPwd, StoreComm '
                      f'FROM Store '
                      f'LEFT JOIN Login on Store.Login_ID = Login.Login_ID '
                      f'LEFT JOIN Source on Store.Source_ID = Source.Source_ID '
                      f'WHERE Store.Login_ID = {getLogin_ID} and '
                      f'Store.Time >= \'{d} 00:00:00.000\' and '
                      f'Time <= \'{e} 00:00:00.000\'')
            cursor.execute(query2)
            decrypt_pwd()


def query_from_all():
    query2 = (f'SELECT Store_ID, SourceName, UserAcc, UserPwd, StoreComm, Time '
              f'FROM Store '
              f'LEFT JOIN Login on Store.Login_ID = Login.Login_ID '
              f'LEFT JOIN Source on Store.Source_ID = Source.Source_ID '
              f'WHERE Store.Login_ID = {getLogin_ID}')
    cursor.execute(query2)
    decrypt_pwd()


def decrypt_pwd():
    table = PrettyTable()
    table.field_names = ['Source Name', 'User Account', 'User Password', 'Comment', 'Time']
    t = 0
    for u in cursor:
        getStore_ID = u[0]
        token = u[3]
        with open(f'{loginAcc}.key', 'r') as g:
            a = g.readlines()
            for b in a:
                c = b.split(':divider:')
                if getStore_ID == int(c[1]):
                    key = c[0]
                    decryptPwd = Fernet(key).decrypt(token)
        table.add_row([u[1], u[2], decryptPwd.decode(), u[4], u[5]])
        t += 1
    print(table)
    if t == 1:
        copy_password(decryptPwd.decode())


def generate_random_password():
    # define list of characters that are chosen to be included in random generation
    characters = []
    # define list of types characters that are chosen to be included
    chosen = []
    # define a list of characters that can be chosen
    strList = [string.ascii_letters, string.digits, string.punctuation]
    # define a list of types of characters that can be chosen with highlight
    charList = ['\x1b[6;30;41m''letters''\x1b[0m', '\x1b[6;30;42m''numbers''\x1b[0m', '\x1b[6;30;43m''symbols''\x1b[0m']
    charListLen = len(charList)
    while True:
        # the valid input count
        a = 0
        # the 'yes' count
        b = 0
        while charListLen != a:
            useChart = input(f'Would you like to include {charList[0 + a]} in the password?(Yes/No):').lower()
            if useChart == 'yes':
                characters.extend(list(strList[0 + a]))
                chosen.append(charList[0 + a])
                a += 1
                b += 1
            elif useChart == 'no':
                a += 1
            else:
                print('Invalid input. Please try again!')
        # when nothing is chosen to be included, loop back to choice
        if b > 0:
            c = ', '.join(chosen)
            print(f'You have chosen {c} to be included in your password')
            break
        else:
            print('You have chosen nothing to be included in your password. Please try again!')
    while True:
        # set up limit for the length to prevent error and exploit
        try:
            length_of_password = int(input('Please enter the length of the password (Min:6, Max:20):'))
            if 6 <= length_of_password <= 20:
                break
            else:
                print('Length of the password must be in between 6 and 20. Please try again!')
        except ValueError:
            print('Length of the password must be a whole number. Please try again!')
    # use string library to get the relevant random choices
    # join each random characters and loop until reaching length of password entered above
    random_password = ''.join(str(random.choice(characters)) for _ in range(length_of_password))
    print(f'Your password is: {random_password}')
    return random_password


def exit_delay_2_second():
    global finish
    finish = True
    conn.close()
    timer = threading.Timer(2, print)
    print('Thank you for using Password Manager')
    timer.start()


while not finish:
    if not login_successful:
        login_menu()
    else:
        function_menu()
