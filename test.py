import stdiomask

login = input('account:')
password = stdiomask.getpass(prompt='password:', mask='*')
print(type(password))
print(login, password)
