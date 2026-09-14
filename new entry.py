# Password Manager new entry
# Author: Yingyi Liao
# For private use only

import pyodbc as odbc
import clipboard
from cryptography.fernet import Fernet


DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'middletohigh'
DATABASE_NAME = 'PasswordManager'
connection_string = f"DRIVER={DRIVER_NAME};\n" \
                    f"SERVER={SERVER_NAME};\n" \
                    f"DATABASE={DATABASE_NAME};\n" \
                    f"Trust_Connection=yes;"
conn = odbc.connect(connection_string)
cursor = conn.cursor()
loginAcc = 'test'


def source():
    while True:
        uSource = str(input('Please enter the source of new entry:'))
        if len(uSource) == 0 or len(uSource.strip(' ')) == 0:
            print('The source can not be blank or contains only white space!\nPlease try again!')
        else:
            break

    query = f'SELECT COUNT(*) FROM Source WHERE (SourceName = \'{uSource}\')'
    cursor.execute(query)
    for x in cursor:
        print(x[0])
        if x[0] > 0:
            return uSource
        else:
            insert_query = f'INSERT INTO Source (SourceName) VALUES (\'{uSource}\')'
            cursor.execute(insert_query)
            conn.commit()
            return uSource


def new_entry_id():
    while True:
        uNewID = str(input('Please enter the new account of new entry:'))
        if len(uNewID) == 0 or len(uNewID.strip(' ')) == 0:
            print('The source can not be blank or contains only white space!\nPlease try again!')
        else:
            return uNewID


def copy_password(x):
    copy_pwd = input('Do you want to copy new password to clipboard?:(Yes/anything else is no)').lower()
    if copy_pwd == 'yes':
        clipboard.copy(x)
        print('The new password has been copied into clipboard!')


def new_entry_pwd():
    while True:
        choice = str(input('Do you want to generate random password? Yes/No')).lower()
        if choice == 'yes':
            uNewPwd = generate_random_password()
            copy_password(uNewPwd)
            return uNewPwd
        elif choice == 'no':
            uNewPwd = str(input('Please enter the new password of new entry:'))
            if len(uNewPwd) == 0 or len(uNewPwd.strip(' ')) == 0:
                print('The source can not be blank or contains only white space!\nPlease try again!')
            else:
                copy_password(uNewPwd)
                return uNewPwd


def encrypt_new_entry_pwd():
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

    query1 = f'SELECT Login_ID FROM Login WHERE (LoginAcc = \'{loginAcc}\')'
    cursor.execute(query1)
    for x in cursor:
        getLogin_ID = x[0]

    query2 = f'SELECT Source_ID FROM Source WHERE (SourceName = \'{uSource}\')'
    cursor.execute(query2)
    for y in cursor:
        getSource_ID = y[0]

    query3 = (f'INSERT INTO Store (Login_ID, Source_ID, UserAcc, UserPwd, StoreComm, Time) '
              f'VALUES (\'{getLogin_ID}\', '
              f'\'{getSource_ID}\', '
              f'\'{newID}\', '
              f'\'{token}\', '
              f'\'{comment}\', '
              f'CURRENT_TIMESTAMP)')

    cursor.execute(query3)
    conn.commit()

    query4 = (f'SELECT * FROM Store '
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
        f.write(key.decode() + ':divider:' + str(getStore_ID) + '\n')

    print('New User Account created successful')
