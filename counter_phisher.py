import datetime
import json
import random
import string
import threading
import uuid

import requests
from requests.exceptions import SSLError

# Added imports
import logging, sys, os, json, time, tqdm
from test_server import srv

class CredentialGenerator:
    def __init__(self):
        self.chars = string.ascii_letters + string.digits
        self.firstname_male = json.loads(open('assets/firstname_male.json').read())
        self.firstname_female = json.loads(open('assets/firstname_female.json').read())
        self.surname = json.loads(open('assets/surnames.json').read())
        self.emails = json.loads(open('assets/emails.json').read())
        self.common_passwords = json.loads(open('assets/common_passwords.json').read())
        self.extensions = json.loads(open('assets/extensions.json').read())
        self.dictionary = json.loads(open('assets/dictionary.json').read())

    def generate_random_firstname_male(self):
        first_name = random.choice(self.firstname_male)
        if random.random() < 0.2:
            if random.random() < 0.5:
                first_name += '-' + random.choice(self.firstname_male)
            else:
                first_name += ' ' + random.choice(self.firstname_male)
        return first_name

    def generate_random_firstname_female(self):
        first_name = random.choice(self.firstname_female)
        if random.random() < 0.2:
            if random.random() < 0.5:
                first_name += '-' + random.choice(self.firstname_female)
            else:
                first_name += ' ' + random.choice(self.firstname_female)
        return first_name

    def generate_random_firstname(self):
        if random.random() < 0.5:
            return self.generate_random_firstname_male()
        else:
            return self.generate_random_firstname_female()

    def generate_random_surname(self):
        return random.choice(self.surname)

    def generate_random_fullname(self):
        first_name = self.generate_random_firstname()
        last_name = self.generate_random_surname()
        return first_name + ' ' + last_name

    def generate_random_word(self):
        return random.choice(self.dictionary)

    def generate_random_password(self):
        event = random.randint(0, 12)
        if event == 0:
            return ''.join(random.choice(self.chars) for _ in range(random.randint(7, 15)))
        elif event in [1, 2]:
            return random.choice(self.dictionary) + random.choice(self.dictionary) + random.choice(string.digits)
        elif event in [3, 4]:
            return random.choice(self.dictionary) + random.choice(string.digits)
        elif event in [5, 6]:
            random.choice(string.digits) + random.choice(self.dictionary) + random.choice(self.generate_random_firstname().lower()).replace(' ', '')
        else:
            return random.choice(self.common_passwords)

    def generate_random_email(self):
        first_name = self.generate_random_firstname()
        last_name = self.generate_random_surname()
        email = random.choice(self.emails)
        extension = random.choice(self.extensions)

        event = random.randint(0, 12)
        if event == [0, 3]:
            return first_name.lower().replace(' ', '_') + '-' + last_name + '@' + email + '.' + extension
        elif event in [4, 7]:
            return first_name.lower().replace(' ', '_') + '_' + last_name.lower().replace(' ', '') + '@' + email + '.' + extension
        elif event in [8, 11]:
            return first_name.lower().replace(' ', '') + self.generate_random_number(length=2) + '@' + email + '.' + extension
        else:
            return first_name.lower().replace(' ', '') + '@' + email + '.' + extension

    def generate_random_digit(self):
        return str(random.randint(0, 9))

    def generate_random_number(self, length=6):
        return ''.join(random.choice(string.digits) for _ in range(length))

    def generate_random_boolean(self):
        return str(random.choice([True, False]))

    def generate_random_word(self):
        return random.choice(self.dictionary)

    def generate_random_letter(self):
        return random.choice(string.ascii_letters)

    def generate_random_string(self, length=6):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def generate_random_date(self):
        return f'{random.randint(1, 31)}/{random.randint(1, 12)}/{random.randint(1900, datetime.date.today().year)}'

    def generate_random_ip(self):
        return f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}'

    def generate_random_url(self):
        return f'https://wwww.{self.generate_random_word()}.{random.choice(self.extensions)}'

    def generate_random_uuid(self):
        return str(uuid.uuid4())


class CredentialTester:
    def __init__(self, target_url, login_form_data):
        self.url = target_url
        self.form_data = login_form_data
        self.success_count = 0
        self.records_sent = 0
        self.successful_requests = []
        self.log_mutex = threading.Lock()
        self.success_count_mutex = threading.Lock()
        self.record_count_mutex = threading.Lock()
        self.success_array_mutex = threading.Lock()
        self.printed_results = False

    def update_success_count(self):
        with self.success_count_mutex:
            self.success_count += 1

    def get_record_number(self):
        with self.record_count_mutex:
            hold = self.records_sent
            self.records_sent += 1
            return hold

    def add_successful_request(self, request):
        with self.success_array_mutex:
            self.successful_requests.append(request)
    def try_credentials(self):
        logger = logging.getLogger("main-app")
        try:
            parsed_form_data = {
                key: (
                    credential_generator.generate_random_email() if '@RANDOM_EMAIL' in value else
                    credential_generator.generate_random_password() if '@RANDOM_PASSWORD' in value else
                    credential_generator.generate_random_digit() if '@RANDOM_DIGIT' in value else
                    credential_generator.generate_random_number() if '@RANDOM_NUMBER' in value else
                    credential_generator.generate_random_boolean() if '@RANDOM_BOOLEAN' in value else
                    credential_generator.generate_random_fullname() if '@RANDOM_NAME' in value else
                    credential_generator.generate_random_firstname() if '@RANDOM_FIRSTNAME' in value else
                    credential_generator.generate_random_firstname_male() if '@RANDOM_FIRSTNAME_MALE' in value else
                    credential_generator.generate_random_firstname_female() if '@RANDOM_FIRSTNAME_FEMALE' in value else
                    credential_generator.generate_random_surname() if '@RANDOM_SURNAME' in value else
                    credential_generator.generate_random_word() if '@RANDOM_WORD' in value else
                    credential_generator.generate_random_letter() if '@RANDOM_LETTER' in value else
                    credential_generator.generate_random_string() if '@RANDOM_STRING' in value else
                    credential_generator.generate_random_date() if '@RANDOM_DATE' in value else
                    credential_generator.generate_random_ip() if '@RANDOM_IP' in value else
                    credential_generator.generate_random_url() if '@RANDOM_URL' in value else
                    credential_generator.generate_random_uuid() if '@RANDOM_UUID' in value else
                    int(value) if isinstance(value, str) and value.isdigit() else
                    float(value) if isinstance(value, str) and value.replace('.', '', 1).isdigit() else
                    value
                )
                for key, value in self.form_data.items()
            }

            r = requests.post(self.url, allow_redirects=False, data=parsed_form_data)

            if r.status_code == 200:
                record_number = self.get_record_number()
                with self.log_mutex:
                    logger.info(f'SUCCESS -- [Record: {record_number}] -- {r.status_code} -- {r.reason} - {parsed_form_data}')
                self.update_success_count()
                self.add_successful_request({'record': record_number, 'form-data': parsed_form_data})
            else:
                with self.log_mutex:
                    logger.warn(f'[Record:{self.records_sent}]{r.status_code} {r.reason} - {parsed_form_data}')
                self.update_records_sent()

        except Exception as e:

            if(not self.printed_results):
                with self.log_mutex:
                    self.printed_results = True

                    logger.info("--------------------")
                    logger.info(f"TOTAL Records Sent: {self.records_sent}. Total Successful Records Sent: {self.success_count}")
                    logger.info(f"Successful Records:\n----------------\n{',\n'.join([json.dumps(x) for x in self.successful_requests])}")
            self.is_running = False
            sys.exit(0)


def run(credential_test, run_event):
    while run_event.is_set():
        credential_test.try_credentials()

if __name__ == '__main__':
    test_server = False
    srv.setup_logger()

    current_directory = os.path.dirname(os.path.realpath(__file__))
    form_data_filename = "form_data.json"
    form_data_file = os.path.join(current_directory, form_data_filename)
    try:
        if sys.argv[1] == '-ts':
            test_server = True
    except Exception:
        pass

    url = None
    if test_server:
        url = 'http://localhost:25565/'
    else:
        url = input('Form URL: ')
    threads = int(input('Threads: '))

    with open(form_data_file, 'r') as f:
        form_data = json.load(f)

    credential_generator = CredentialGenerator()
    credential_tester = CredentialTester(url, form_data)
    running_threads = []

    try:
        run_event = srv.threading.Event()
        run_event.set()
        logger = srv.logging.getLogger("main-app")
        logger.info(f"Starting with {threads} threads and URL: {url}...")
        for _ in range(threads):
            t = threading.Thread(target=run, args=(credential_tester, run_event,))
            t.start()
            running_threads.append(t)

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt detected... Shutting down threads...")
        run_event.clear()
        for i in tqdm(running_threads):
            i.join()

        if(not credential_tester.printed_results):
            with credential_tester.log_mutex:
                credential_tester.printed_results = True
                logger.info("--------------------")
                logger.info(f"TOTAL Records Sent: {credential_tester.records_sent}. Total Successful Records Sent: {credential_tester.success_count}")
                logger.info(f"Successful Records:\n----------------\n{',\n'.join([json.dumps(x) for x in credential_tester.successful_requests])}")