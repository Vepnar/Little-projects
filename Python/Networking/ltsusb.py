#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
Author: Arjan de Haan (Vepnar)
Version: 0.1
Hardware: Huawei E3372 (Lte usb stick)
Requirements:
    xmltodict
    requests
    datetime
"""
from datetime import datetime
import json
import xmltodict
import requests

class HuaweiDriver:
    """Script to send sms messages from the Huawei E3372"""

    def __init__(self, ip='192.168.8.1'):
        self._router_ip = ip
        self._headers = {'Content-Type': 'text/xml; charset=UTF-8'}

        # Receive token and cookie
        code, xml = self._make_request('api/webserver/SesTokInfo')
        if code != 200:
            raise Exception(f'Token request returned {code} instead of 200')

        self._headers.update({
            'Cookie' : xml['SesInfo'],
            '__RequestVerificationToken' : xml['TokInfo']
            })

        self._xheaders = {
            'Content-Type': 'text/xml; charset=UTF-8',
            'Cookie' : xml['SesInfo'],
            '__RequestVerificationToken' : xml['TokInfo'],
            'X-Requested-With' : 'XMLHttpRequest'
        }

    def _make_request(self, link, post=False):
        """Make a request to the router.

        Args:
            link: path
            post: False when get request, string when a post request

        Returns: (dict) response of the request

        Raises:
            Exception when can't be parsed into a dict
            Or other exceptions when there are network problems
        """
        url = f'http://{self._router_ip}/{link}'

        # Make a post request when asked for it
        if post:
            request_answer = requests.post(
                url, headers=self._xheaders, allow_redirects=False, data=post)
        else:
            request_answer = requests.get(url, headers=self._headers, allow_redirects=False)

        # Raise error
        xml = xmltodict.parse(request_answer.text)
        if 'response' not in xml:
            raise Exception(self._pretty_print(xml))
        xml = xml['response']
        return request_answer.status_code, xml

    def _pretty_print(self, dict_to_show):
        """Print a dict pretty in the terminal"""
        dict_to_show = json.dumps(dict_to_show, indent=4, sort_keys=True)
        print(dict_to_show)

    def pin_status(self):
        """Receive information about the simcard.

        Returns: (dict)
            PinOptState
            SimPinTimes
            PimPukTimes
            SimState
        """

        _, code = self._make_request('api/pin/status')
        self._pretty_print(code)

    def get_traffic(self):
        """Receive network traffic from the simcard

        Return: (dict) network traffic
        """

        _, code = self._make_request('api/monitoring/traffic-statistics')
        return code

    def send_sms(self, number, message):
        """Send sms to given phone number

        args:
            number: (str) phone number of device the sms should be send to.
            message: (str) The body of the message (totally unexpected)
        """

        # Prepare xml data
        data = '<request><Index>-1</Index>'
        data += f'<Phones><Phone>{number}</Phone></Phones>'
        data += '<Sca></Sca>'
        data += f'<Content>{message}</Content><Length>{len(message)}</Length>'
        data += '<Reserved>1</Reserved>'
        data += '<Date>{}</Date>'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data += '</request>'

        _ = self._make_request('api/sms/send-sms', post=data)

def main(number, message):
    """Will create the driver object and send an sms"""
    huawei_driver = HuaweiDriver()
    huawei_driver.send_sms(number, message)

if __name__ == '__main__':
    main('+31612345678', 'Hello World!\nPython')
