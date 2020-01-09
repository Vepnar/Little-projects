#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bust usernames of a given user easy and async, dont execute this script on me please :)
Author: Arjan de Haan (Vepnar)
Lasted edited: 9 January 2020
Version: 0.1
"""
import re
import json
import random
import argparse
import grequests

HEADERS = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
class Website:
    """Class to store sites
    args:
        object parsed from default json file
    """

    def __init__(self, json_object):
        self._name = json_object['name']
        self._domain = json_object['domain']
        self._response = json_object['response']
        self._confirmed = False

        switcher = {
            'status_code' : self._status_code,
            'not_status_code' : self._not_status_code,
            'not_regex_contains' : self._not_regex_contains
        }

        self.process_response = switcher[json_object['validationType']]

    def _status_code(self, response):
        """Check if the status code is the same"""
        self._confirmed = response.status_code == self._response

    def _not_status_code(self, response):
        """Check if the status code is not the same"""
        self._confirmed = response.status_code is not self._response
    def _regex_contains(self, response):
        """Check is there is a match"""
        self._confirmed = re.search(self._response, response.text) is not None
    def _not_regex_contains(self, response):
        """Check if  there is not a match"""
        self._confirmed = re.search(self._response, response.text) is None

    def get_domain(self, username):
        """Receive domain with formatted username in it"""
        return self._domain.format(username=username)

    def get_if_exists(self, username):
        """Return url when exists"""
        if self._confirmed:
            return self.get_domain(username)
        return None

    def __str__(self):
        """Convert class to a string"""
        if self._confirmed:
            return '[x] {}'.format(self._name)
        return '[ ] {}'.format(self._name)

def websites_from_json(file_path='sites.json'):
    """Create website objects from a json file"""
    with open(file_path, 'r') as json_file:
        content = ''.join(json_file.readlines())
    json_objects = json.loads(content)

    websites = []
    for json_object in json_objects:
        websites.append(Website(json_object))
    return websites

def get_random_headers():
    """Get a random user agent to dodge the bot protection on most of the sites"""
    return {
        'User-Agent': random.choice(HEADERS),
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

def receive_async(websites, username):
    """Run async through all the websites and check if the user exists

    Returns: list of strings with existing websites (username formatting into the string)
    """
    async_list = []
    for website in websites:
        action_item = grequests.get(
            website.get_domain(username), hooks={'response' : website.process_response},
            headers=get_random_headers(), allow_redirects=False)
        async_list.append(action_item)

    grequests.map(async_list)

    sites = []
    for website in websites:
        domain = website.get_if_exists(username)
        if domain is not None:
            sites.append(domain)
    return sites

def main():
    """Main function that will run when this script is run"""
    parser = argparse.ArgumentParser(description='Try to find all accounts matching the given name')
    parser.add_argument(
        'username', metavar='username', type=str, help='username without spaces')
    args = parser.parse_args()

    sites = websites_from_json()
    exist = receive_async(sites, args.username)

    for site in exist:
        print(site)

if __name__ == "__main__":
    main()
