# Counter Phishing Tool

This project is an offensive and proactive tool designed to disrupt phishing attacks by flooding fake phishing websites' login portals with a deluge of fake user data. It's a tool crafted for cybersecurity professionals to actively combat and mitigate risks associated with phishing attacks.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

## Introduction
The Counter Phishing Tool is a Python-based tool tailored to inundate phishing websites with fake credentials. By proactively overwhelming them with bogus data, it aims to disrupt and thwart phishing scams before they can ensnare unsuspecting users.

## Features
- **Credential Generation**: Generates a plethora of random names, emails, passwords, etc., to mimic real users.
- **Automated Login Attempts**: Automatically bombards login pages of phishing websites with the generated credentials.
- **Configurable Threads**: Supports threading for efficient parallel processing.
- **Customizable**: Allows customization of the login form data payload.

## Scriptable formdata payload
The `form_data.json` file contains the payload to be sent to the phishing website's login form. The payload should be modified according to the login form fields of the phishing website. The following is an example of a payload for a login form with fields for `email` and `password`:

### Example
```json
{
  "foo": 69,
  "email": "@RANDOM_EMAIL",
  "password": "@RANDOM_PASSWORD",
  "bar": false
}
```

### Supported Keywords
- `@RANDOM_PASSWORD`: Generates a random password.
- `@RANDOM_EMAIL`: Generates a random email address.
- `@RANDOM_NUMBER`: Generates a random number.
- `@RANDOM_DIGIT`: Generates a random digit.
- `@RANDOM_BOOLEAN`: Generates a random boolean.
- `@RANDOM_FULLNAME`: Generates a random full name.
- `@RANDOM_FIRSTNAME`: Generates a random first name.
- `@RANDOM_FIRSTNAME_MALE`: Generates a random male first name.
- `@RANDOM_FIRSTNAME_FEMALE`: Generates random female first name.
- `@RANDOM_SURNAME`: Generates a random surname.
- `@RANDOM_WORD`: Generates a random word.
- `@RANDOM_LETTER`: Generates a random letter.
- `@RANDOM_IP`: Generates a random IP address.
- `@RANDOM_URL`: Generates a random URL.
- `@RANDOM_UUID`: Generates a random UUID.

## Setup
1. **Clone the Repository**: `git clone https://github.com/EwyBoy/Counter-Phishing-Tool.git`
2. **Install Dependencies**: Ensure you have Python installed. Install necessary dependencies via `pip install -r requirements.txt`.
3. **Prepare Form Data**: Modify the `form_data.json` file according to the phishing website's login form fields.
4. **Run the Script**: Execute the script by running `python counter_phisher.py`.

## Usage
1. **Enter Phishing Website URL**: Provide the URL of the fake phishing website's login portal you want to target.
2. **Set Number of Threads**: Specify the number of threads to be used for targeting.
3. **Review Results**: Examine the console output for potential successful login attempts or error messages indicating unreachable URLs.

## Contributing
Contributions are encouraged! If you encounter any issues or have ideas for enhancements, feel free to open an issue or submit a pull request.

## Disclaimer
This tool is provided as is. I do not take any responsibility for how you choose to use this tool. It is your responsibility to use it responsibly and ethically.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
