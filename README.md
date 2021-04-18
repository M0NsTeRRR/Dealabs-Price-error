[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d071f01d0d074b1aaa718747cc6b787b)](https://www.codacy.com/manual/M0NsTeRRR/Dealabs-Price-error?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=M0NsTeRRR/Dealabs-Price-error&amp;utm_campaign=Badge_Grade)

The goal of this project is to get an email when a new price error appear on Dealabs (https://www.dealabs.com/). 
You must have Dealabs permission to use this software.

## Requirements
#### Classic
- Python >= 3.7
- Pip3

#### Docker
- Docker CE

## Install

- Tested with a gmail account
- You must provide your email and a password application (https://myaccount.google.com/apppasswords)

### Classic
Install the requirements `pip install -r requirements.txt`

Fill config.json with some informations :
```json
{
  "topic": "https://www.dealabs.com/discussions/le-topic-des-erreurs-de-prix-1056379",
  "page": 300,
  "delay": 60,
  "email": {
    "email-sender": {
      "smtp_domain": "smtp.gmail.com",
      "smtp_port": 587,
      "smtp_email": "myemail1@gmail.com",
      "smtp_password": "myawesomepassword"
    },
    "email-receivers": [
      "myemail1@gmail.com",
      "myemail2@hotmail.com"
    ]
  }
}
```
Start the script `python main.py`

### Docker

Docker version support only one email receiver (start many containers to fix the problem)

Fill environment variables

`docker run -d --restart=always -e "DEALABS_TOPIC=" -e "DEALABS_PAGE=" -e "DEALABS_DELAY=" -e "DEALABS_SMTP_DOMAIN=" 
-e "DEALABS_SMTP_PORT=" -e "DEALABS_SMTP_EMAIL=" -e "DEALABS_SMTP_PASSWORD=" -e "DEALABS_EMAIL_RECEIVER=" monsterrr/dealabs-price-error:latest`

# Licence

The code is under CeCILL license.

You can find all details here: https://cecill.info/licences/Licence_CeCILL_V2.1-en.html

# Credits

Copyright © Ludovic Ortega, 2019

Contributor(s):

-Ortega Ludovic - ludovic.ortega@adminafk.fr
