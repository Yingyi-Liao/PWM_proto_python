# Password Manager random generator
# Author: Yingyi Liao
# For private use only


import string
import random


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


generate_random_password()
