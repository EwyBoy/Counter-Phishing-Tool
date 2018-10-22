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

emails = [
    "gmail.com", "yahoo.com", "hotmail.com", "live.com", "me.com",
    "msn.com", "aol.com", "verizon.net", "optonline.net", "att.net",
    "sbcglobal.net", "outlook.com", "icloud.com", "online.no", "auf.de"
]

names = json.loads(open('assets/names.json').read())

for name in names:
    name_extra = ''.join(random.choice(string.digits))
    username = name.lower() + name_extra + '@' + emails[random.randint(0, len(emails) - 1)]
    password = ''.join(random.choice(chars) for i in range(8))

    try:
        requests.post(url, allow_redirects=False, data={
            str(formDataNameLogin): username,
            str(formDataNamePass): password
        })

        print 'Sending username: %s and password %s' % (username, password)

    except SSLError as e:
        print 'Error: URL can no long be reach..'



