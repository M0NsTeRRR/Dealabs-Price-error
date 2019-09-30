[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d071f01d0d074b1aaa718747cc6b787b)](https://www.codacy.com/manual/M0NsTeRRR/Dealabs-Price-error?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=M0NsTeRRR/Dealabs-Price-error&amp;utm_campaign=Badge_Grade)
[![Docker Automated build](https://img.shields.io/docker/cloud/automated/monsterrr/dealabs-price-error?style=flat-square)](https://hub.docker.com/r/monsterrr/dealabs-price-error)
[![Docker Build Status](https://img.shields.io/docker/cloud/build/monsterrr/dealabs-price-error?style=flat-square)](https://hub.docker.com/r/monsterrr/dealabs-price-error)

The goal of this project is to get an email when a new price error appear on Dealabs (https://www.dealabs.com/). 
You must have Dealabs permission to use this software.

## Requirements
#### Classic
- Python >= 3.7
- Pip3

#### Docker
- Docker CE

## Install

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
      "myemail2@gmail.com"
    ]
  }
}
```
Start the script `python main.py`

### Docker

TO DO

# Licence

The code is under CeCILL license.

You can find all details here: http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html

# Credits

Copyright © Ludovic Ortega, 2019

Contributor(s):

-Ortega Ludovic - mastership@hotmail.fr
