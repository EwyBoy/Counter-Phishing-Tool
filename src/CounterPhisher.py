import requests
import os
import random
import string
import json

from requests.exceptions import SSLError

url = raw_input('URL: ')
formDataNameLogin = raw_input('Form Data [Account/Email] Name: ')
formDataNamePass = raw_input('Form Data Password Name: ')

chars = string.ascii_letters + string.digits
random.seed = (os.urandom(1024))

names = json.loads(open('assets/names.json').read())
emails = json.loads(open('assets/emails.json').read())
ext = json.loads(open('assets/extensions.json').read())
dictionary = json.loads(open('assets/dictionary.json').read())


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
    event = random.randint(0, 4)

    if event == 0:
        return ''.join(random.choice(chars) for i in range(random.randint(7, 15)))
    elif event in [1, 2]:
        return random.choice(dictionary) + random.choice(dictionary) + random.choice(string.digits)
    else:
        return random.choice(string.digits) + random.choice(dictionary) + random.choice(names)


while True:
    username = generateRandomName() + '@' + random.choice(emails) + '.' + random.choice(ext)
    password = generateRandomPassword()

    try:

        r = requests.post(url, allow_redirects=False, data={
            str(formDataNameLogin): username,
            str(formDataNamePass): password,
            #'formimage1.x': 135 + random.randint(-20, 20),
            #'formimage1.y': 26 + random.randint(-20, 20)
        })

        print r.status_code
        print 'Sending username: %s with password %s' % (username, password)

        if r.status_code > 400:
            print ('HTTP Error code: %s' % r.status_code)
            break

    except SSLError as e:
        print 'Error: URL can no long be reach..'
