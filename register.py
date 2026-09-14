# Password Manager register
# Author: Yingyi Liao
# For private use only

import pyodbc as odbc
import hashlib


def new_account():
    while True:
        newAcc = str(input('Please enter your new login account:'))
        if len(newAcc) == 0:
            print('New login account can not be blank!\nPlease try again!')
        elif newAcc != ''.join(_ for _ in newAcc if _.isalnum()):
            print('Account can not contain space or special characters!\nPlease try again!')
        else:
            DRIVER_NAME = 'SQL Server'
            SERVER_NAME = 'middletohigh'
            DATABASE_NAME = 'PasswordManager'
            connection_string = f"DRIVER={DRIVER_NAME};\n" \
                                f"SERVER={SERVER_NAME};\n" \
                                f"DATABASE={DATABASE_NAME};\n" \
                                f"Trust_Connection=yes;"
            conn = odbc.connect(connection_string)
            cursor = conn.cursor()

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
                if len(newPwd) == 0:
                    print('New login password can not be blank!\nPlease try again!')
                else:
                    return newPwd
        else:
            print('Invalid input!\nPlease try again!')


def register():
    newAcc = new_account()
    newPwd = hashlib.sha256((new_password()).encode()).hexdigest()
    DRIVER_NAME = 'SQL Server'
    SERVER_NAME = 'middletohigh'
    DATABASE_NAME = 'PasswordManager'
    connection_string = f"DRIVER={DRIVER_NAME};\n" \
                        f"SERVER={SERVER_NAME};\n" \
                        f"DATABASE={DATABASE_NAME};\n" \
                        f"Trust_Connection=yes;"
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    query = f'INSERT INTO Login (LoginAcc, LoginPwd) VALUES (\'{newAcc}\', \'{newPwd}\')'
    print(query)
    cursor.execute(query)
    conn.commit()
    print('New login created successful!')
