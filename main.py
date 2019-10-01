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
from json import load, loads
from sys import exit as sys_exit
from time import sleep
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import smtplib

from bs4 import BeautifulSoup
from cfscrape import create_scraper

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# get configuration from environment variables
config = {
    "topic": str(environ.get("DEALABS_TOPIC", "https://www.dealabs.com/discussions/le-topic-des-erreurs-de-prix-1056379")),
    "page": int(environ.get("DEALABS_PAGE", "300")),
    "delay": int(environ.get("DEALABS_DELAY", "60")),
    "email": {
        "email-sender": {
          "smtp_domain": str(environ.get("DEALABS_SMTP_DOMAIN", "smtp.gmail.com")),
          "smtp_port": int(environ.get("DEALABS_SMTP_PORT", "587")),
          "smtp_email": str(environ.get("DEALABS_SMTP_EMAIL", "")),
          "smtp_password": str(environ.get("DEALABS_SMTP_PASSWORD", ""))
        },
        "email-receivers": [
          str(environ.get("DEALABS_EMAIL_RECEIVER", ""))
        ]
    }
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
    if "smtp_domain" not in config["email"]["email-sender"] or not isinstance(config["email"]["email-sender"]["smtp_domain"], str):
        raise Exception("config.json not filled properly")
    if "smtp_port" not in config["email"]["email-sender"] or 1 < config["delay"] > 65535:
        raise Exception("config.json not filled properly")
    if "smtp_email" not in config["email"]["email-sender"] or not isinstance(config["email"]["email-sender"]["smtp_email"], str):
        raise Exception("config.json not filled properly")
    if "smtp_password" not in config["email"]["email-sender"] or not isinstance(config["email"]["email-sender"]["smtp_password"], str):
        raise Exception("config.json not filled properly")
except Exception as error:
    logger.error(f'{error}')
    sys_exit(1)


def get_mail_content(deal):
    price_error_links = comments[-1].find('div', {"class": "comment-body"}) \
                                    .find('div', {"class": "userHtml-content"}) \
                                    .find_all('a')
    formatted_error_links = ""
    for link in price_error_links:
        formatted_error_links += link["title"] + "\n"

    comment_link = loads(
        deal.find('div', {"class": "comment-footer"})
            .find_all('button')[-1]
            .get('data-popover')
    )['tplData']['url']
    comment_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text = f"""
    Links :
    {formatted_error_links}
    ----------------------------------------
    Timestamp : {comment_timestamp}
    Dealabs link : {comment_link}
    """

    return f'Subject: "New Dealabs Price error"\n\n{text}'


def send_mail(deal):
    server_smtp = smtplib.SMTP(config["email"]["email-sender"]["smtp_domain"],
                               config["email"]["email-sender"]["smtp_port"])
    server_smtp.ehlo()
    server_smtp.starttls()
    server_smtp.login(config["email"]["email-sender"]["smtp_email"], config["email"]["email-sender"]["smtp_password"])
    server_smtp.sendmail("Dealabs-Price-error", config["email"]["email-receivers"], get_mail_content(deal))
    server_smtp.close()


last_price_error = []
scraper = create_scraper()

while True:
    try:
        new_page_dectected = False
        url = config["topic"] + "?page=" + str(config["page"])

        # scrap the page
        r = scraper.get(url)

        # set the current page in case of redirection
        config["page"] = parse_qs(urlparse(r.url).query)["page"][0]

        logger.debug(f'url = {r.url}')
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
            # get list of ID of price error comments
            price_error_list = [comment.get('id') for comment in comments]

            # at boot init the list
            if not last_price_error:
                last_price_error = price_error_list[-40:]

            # check if the Price error was already registered in cache
            if comments[-1].get('id') in last_price_error:
                logger.info(f'Price error already registered (comment={comments[-1].get("id")})')
            else:
                if last_price_error[-1] in price_error_list[-40:]:
                    first_price_error = price_error_list.index(last_price_error[-1]) + 1
                else:
                    first_price_error = 0
                for index_price_error in range(first_price_error, len(comments)):
                    logger.info(f'New price error detected (comment={comments[index_price_error].get("id")})')
                    send_mail(comments[index_price_error])
            last_price_error = price_error_list[-40:]
            sleep(config["delay"])
    except Exception as error:
        logger.error(f'{error}')
