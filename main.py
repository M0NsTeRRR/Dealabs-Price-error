# ----------------------------------------------------------------------------
# Copyright © Ludovic Ortega, 2019
#
# Contributeur(s):
#     * Ortega Ludovic - mastership@hotmail.fr
#
# Ce logiciel, Dealabs-Price-error, est un programme informatique servant à avertir
# l'utilisateur d'une erreur de prix.
#
# Ce logiciel est régi par la licence CeCILL soumise au droit français et
# respectant les principes de diffusion des logiciels libres. Vous pouvez
# utiliser, modifier et/ou redistribuer ce programme sous les conditions
# de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA
# sur le site "http://www.cecill.info".
#
# En contrepartie de l'accessibilité au code source et des droits de copie,
# de modification et de redistribution accordés par cette licence, il n'est
# offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
# seule une responsabilité restreinte pèse sur l'auteur du programme,  le
# titulaire des droits patrimoniaux et les concédants successifs.
#
# A cet égard  l'attention de l'utilisateur est attirée sur les risques
# associés au chargement,  à l'utilisation,  à la modification et/ou au
# développement et à la reproduction du logiciel par l'utilisateur étant
# donné sa spécificité de logiciel libre, qui peut le rendre complexe à
# manipuler et qui le réserve donc à des développeurs et des professionnels
# avertis possédant  des  connaissances  informatiques approfondies.  Les
# utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
# logiciel à leurs besoins dans des conditions permettant d'assurer la
# sécurité de leurs systèmes et ou de leurs données et, plus généralement,
# à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.
#
# Le fait que vous puissiez accéder à cet en-tête signifie que vous avez
# pris connaissance de la licence CeCILL, et que vous en avez accepté les
# termes.
# ----------------------------------------------------------------------------

import logging
from os import environ
from json import load
from sys import exit as sys_exit
from time import sleep
from bs4 import BeautifulSoup
from cfscrape import create_scraper
import smtplib

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# get configuration from environment variables
config = {
    "topic": int(environ.get("DEALABS_TOPIC", "1800")),
    "page": int(environ.get("DEALABS_PAGE", "0")),
    "delay": int(environ.get("DEALABS_DELAY", "180"))
}

# get configuration from file
try:
    with open('config.json') as json_data_file:
        config.update(load(json_data_file))
except FileNotFoundError:
    pass
except Exception as e:
    logger.error("{error}".format(error=e))
    sys_exit(1)

try:
    if "topic" not in config or not isinstance(config["topic"], str):
        raise Exception("config.json not filled properly")
    if "page" not in config or not isinstance(config["page"], int) or config["page"] < 0:
        raise Exception("config.json not filled properly")
    if "delay" not in config or 60 <= config["delay"] >= 3600:
        raise Exception("config.json not filled properly")
except Exception as e:
    logger.error("{error}".format(error=e))
    sys_exit(1)

last_price_error = ""
scraper = create_scraper()

while True:
    try:
        new_page_dectected = False
        url = config["topic"] + "?page=" + str(config["page"])

        # scrap the page
        r = scraper.get(url)
        logger.debug(f'url = {url}')
        soup = BeautifulSoup(r.content, 'html.parser')

        # get all Price error
        comments = soup.find_all('article', {"class": "comments-list-item"})

        # check if there is a new page
        next_page = soup.find('a', {"class": "pagination-next"})

        if next_page is not None:
            new_page_dectected = True
            config["page"] += 1
            logger.info(f'New page detected (page={config["page"]})')
            sleep(1)
        else:
            if last_price_error != comments[-1].get('id'):
                logger.info(f'New price error detected (comment={comments[-1].get("id")})')
                server_smtp = smtplib.SMTP(config["email"]["email-sender"]["smtp_domain"], config["email"]["email-sender"]["smtp_port"])
                server_smtp.ehlo()
                server_smtp.starttls()
                server_smtp.login(config["email"]["email-sender"]["smtp_email"], config["email"]["email-sender"]["smtp_password"])
                server_smtp.sendmail("Dealabs-Price-error", config["email"]["email-receivers"], "New DEAL")
                server_smtp.close()
            sleep(config["delay"])
        last_price_error = comments[-1].get('id')
    except Exception as e:
        logger.error("{error}".format(error=e))
