__author__ = 'jhoelzer'


from bs4 import BeautifulSoup
import requests
import re
import argparse
import sys


def web_scraper(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def find_urls(soup):
    url_scraper = set()
    url_regex = r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    url_tags = soup.find_all('a', href=True)

    for url in url_tags:
        if re.search(url_regex, str(url)):
            url_scraper.add(url.get('href'))

    if not url_scraper:
        print('No urls found')

    print('\n'.join(url_scraper))
    return url_scraper


def find_emails(soup):
    email_scraper = set()
    email_regex = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    email_tags = soup.find_all('a')

    for email in email_tags:
        if re.search(email_regex, str(email)):
            email_scraper.add(email.get('href').replace('mailto:', ''))

    if not email_scraper:
        print('No emails found')

    print('\n'.join(email_scraper))
    return email_scraper


def find_phones(soup):
    phone_scraper = set()
    phone_regex = re.compile(
        r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?')
    phones = phone_regex.findall(str(soup))

    for phone in phones:
        if phone not in phone_scraper:
            phone_scraper.add(
                '({}) {}-{}'.format(phone[0], phone[1], phone[2]))

    if not phone_scraper:
        print('No phone numbers found')

    print('\n'.join(phone_scraper))
    return phone_scraper


def find_images(soup):
    image_scraper = set()
    images = soup.find_all('img', src=True)

    for image in images:
        image_scraper.add(image.get('src'))

    if not image_scraper:
        print('No images found')

    print('\n'.join(image_scraper))
    return image_scraper


def create_parser():
    parser = argparse.ArgumentParser(
        description='Perform transformation on input text.')
    parser.add_argument('url', help='enter url')
    return parser


def main(args):
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    namespace = parser.parse_args(args)
    souped = web_scraper(namespace.url)

    if souped:
        print('URLs:')
        find_urls(souped)
        print('Emails:')
        find_emails(souped)
        print('Phone Numbers:')
        find_phones(souped)
        print('Images:')
        find_images(souped)


if __name__ == '__main__':
    main(sys.argv[1:])
