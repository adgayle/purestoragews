#!/usr/bin/env python
'''Pure Storage alerts, volumes and snapshot integration library
'''
from __future__ import print_function
import logging
from json import loads
from requests import session, ConnectionError, Timeout


def login(array, api_token):
    '''Login to the array with the api_token

    Args:
        array (string) is the name of the PureStorage array
        api_token (string) is the API token authentication string

    Returns:
        session (requests.sessions.Session) http session to preserve the login
        result (boolean) True if login successful, False if login failed
    '''
    url = 'https://' + array + '/api/1.8/auth/session'
    payload = {}
    payload['api_token'] = api_token
    req_session = session()

    result = False
    try:
        response = req_session.post(
            url,
            verify=False,
            data=payload,
            timeout=30
        )
        if response.status_code == 200:
            logging.debug('The login was successful with response %s', response.text)
            result = True
        else:
            logging.critical('The login failed with response %s', response.text)

    except ConnectionError:
        logging.exception('Failed to login with API token')
    except Timeout:
        logging.exception('Failed to login to %s due to timeout', array)

    return req_session, result


def get_alerts(array, api_token):
    '''Retrieve open alerts from the array

    Args:
        array (string) is the name of the PureStorage array
        api_token (string) is the API token authentication string

    Returns:
        messages (json list) containing all the open messages on the array
    '''
    messages = None
    req_session, logged_in = login(array, api_token)
    if logged_in:
        parameters = '?open=true&recent=true'
        url = 'https://' + array + '/api/1.8/message' + parameters
        try:
            response = req_session.get(
                url,
                verify=False,
                timeout=30
            )
            if response.status_code == 200:
                logging.debug('Successfully retrieved messages %s', response.text)
                messages = loads(response.text)
            else:
                logging.critical('Failed to retrieve messages with response %s', response.text)

        except ConnectionError:
            logging.exception('Unable to call API to retrieve messages')
        except Timeout:
            logging.exception('Timeout for message retrieve reached for array %s', array)

    return messages


def get_volumes(array_name, api_token):
    '''Gets a list of the volumes on the array

    Args:
        array_name (string) with the name of the Pure Storage array
        api_token (string) access token for the Pure Storage array

    Returns:
        A (list) of array volumes and serial number
    '''
    results = []
    req_session, logged_in = login(array_name, api_token)
    if logged_in:
        parameters = '?pending=false'
        url = 'https://' + array_name + '/api/1.8/volume' + parameters
        try:
            response = req_session.get(
                url,
                verify=False,
                timeout=30
            )
            if response.status_code == 200:
                logging.debug('Successfully retrieved volumes %s', response.text)
                volumes = loads(response.text)
                for volume in volumes:
                    vol_attr = (volume['name'], volume['serial'])
                    results.append(vol_attr)
            else:
                logging.critical('Failed to retrieve volumes with response %s', response.text)

        except ConnectionError:
            logging.exception('Unable to call API to retrieve volumes')
        except Timeout:
            logging.exception('Timeout for volume retrieve reached for array %s', array_name)
        except KeyError:
            logging.exception('No volumes were returned')

    return results


def get_snapshots(array_name, api_token):
    '''Gets a list of the snapshots on the array

    Args:
        array_name (string) with the name of the Pure Storage array
        api_token (string) access token for the Pure Storage array

    Returns:
        A (list) of array snapshots and serial number
    '''
    results = []
    req_session, logged_in = login(array_name, api_token)
    if logged_in:
        parameters = '?snap=true'
        url = 'https://' + array_name + '/api/1.8/volume' + parameters
        try:
            response = req_session.get(
                url,
                verify=False,
                timeout=30
            )
            if response.status_code == 200:
                logging.debug('Successfully retrieved snapshots %s', response.text)
                snapshots = loads(response.text)
                for snapshot in snapshots:
                    snap_attr = (snapshot['name'], snapshot['serial'])
                    results.append(snap_attr)
            else:
                logging.critical('Failed to retrieve snapshots with response %s', response.text)

        except ConnectionError:
            logging.exception('Unable to call API to retrieve snapshots')
        except Timeout:
            logging.exception('Timeout for snapshot retrieve reached for array %s', array_name)
        except KeyError:
            logging.exception('No snapshot were returned')

    return results
