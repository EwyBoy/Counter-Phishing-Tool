#! /usr/bin/env python3

import requests
import os
import random
import string
import json
import threading
from requests.exceptions import SSLError


def generateRandomName():
    event = random.randint(0, 4)

    if event == 0:
        return str(random.choice(names)).lower()
    elif event in [1, 2]:
        separator = ['-', '.', '_']
        return str(random.choice(names)).lower() + separator[random.randint(0, len(separator) - 1)] + str(
            random.choice(names)).lower()
    else:
        return str(random.choice(names)).lower() + random.choice(string.digits) + random.choice(string.digits)


def generateRandomPassword():
    event = random.randint(0, 6)

    if event == 0:
        return ''.join(random.choice(chars) for i in range(random.randint(7, 15)))
    elif event in [1, 2]:
        return random.choice(dictionary) + random.choice(dictionary) + random.choice(string.digits)
    elif event in [3, 4]:
        return random.choice(dictionary) + random.choice(string.digits)
    else:
        return random.choice(string.digits) + random.choice(dictionary) + random.choice(names)


def run():
    while True:
        username = generateRandomName() + '@' + random.choice(emails) + '.' + random.choice(ext)
        password = generateRandomPassword()

        try:
            r = requests.post(url, allow_redirects=False, data={
                str(formDataNameLogin): username,
                str(formDataNamePass): password,
            })

            print(r.status_code)
            print('Sending username: %s with password %s' % (username, password))
            print(url + '\n')

            if r.status_code > 400:
                print('HTTP Error code: %s' % r.status_code)
                input()
                exit()

        except SSLError as e:
            print('Error: URL can no longer be reached..')
        except Exception as e:
            print('Error: {0}'.format(e))


if __name__ == '__main__':
    url = input('Form URL: ')
    formDataNameLogin = input('Form Data [Account/Email] Name: ')
    formDataNamePass = input('Form Data Password Name: ')
    threads = int(input('Threads: '))

    chars = string.ascii_letters + string.digits
    random.seed = (os.urandom(1024))

    names = json.loads(open('assets/names.json').read())
    emails = json.loads(open('assets/emails.json').read())
    ext = json.loads(open('assets/extensions.json').read())
    dictionary = json.loads(open('assets/dictionary.json').read())

    for i in range(threads):
        t = threading.Thread(target=run)
        t.start()
