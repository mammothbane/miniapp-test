#!/usr/bin/env python3

import websockets

import asyncio
import json
import logging
import random
import string

CREDS_SEARCH = 'credentials_search'
CREDS_SUGGEST = 'credentials_suggest'
CREDS_REQUEST = 'request_credential'
CREDS_PROVIDE = 'provide_credential'
CREDS_STORE = 'credentials_store'
CREDS_COMMIT = 'credentials_commit'
CREDS_ABORT = 'credentials_abort'
EXT_CLICKED = 'ext_icon_clicked'
NAVIGATE = 'navigate'
LOCK_CHECK = 'valt_lock_check'
LOCK_STATE = 'valt_lock_state'

random_chars = string.ascii_letters + string.digits
tlds = ['com', 'net', 'org', 'edu', 'io', 'se', 'co.uk', 'biz']

logging.basicConfig(level=logging.INFO)
logging.getLogger('websockets').setLevel(logging.INFO)

def random_string(lower=5, upper=15):
    return ''.join(random.choices(random_chars, k=random.randint(lower, upper)))

def random_email():
    return '{}@{}.{}'.format(random_string(4, 11), random_string(4, 8), random.choice(tlds))

def random_creds(count=1):
    return [{'username': random_email(), 'uuid': random_string(), 'title': random_string(), 'site': random_string()} for _ in range(count)]

async def serve(sock, path):
    logging.info('handling socket %s at path %s', sock, path)
    while True:
        logging.debug('awaiting data')
        msg = await sock.recv()
        logging.debug('received message: %s', msg)

        data = json.loads(msg)['data']
        if 'command' not in data:
            logging.error('no command type found in message')
            continue

        cmd = data['command'].lower()

        if cmd == CREDS_SEARCH:
            logging.debug('received SEARCH')
            ret = {
                'command': CREDS_SUGGEST,
                'credentials': random_creds(random.randint(2, 6)),
                'session': data['session'],
            }

            await sock.send(json.dumps(ret))
            logging.debug('sent SUGGEST')

        if cmd == CREDS_REQUEST:
            logging.debug('received REQUEST')
            ret = {
                'command': CREDS_PROVIDE,
                'credential': {
                    'username': random_email(),
                    'uuid': data['uuid'],
                    'title': random_string(),
                    'site': random_string(),
                    'password': random_string()
                },
                'session': data['session']
            }
            await sock.send(json.dumps(ret))
            logging.debug('sent PROVIDE')

        if cmd == LOCK_CHECK:
            logging.debug('received LOCK_CHECK')
            ret = {
                'command': LOCK_STATE,
                'locked': False,
                'session': data['session']
            }
            await sock.send(json.dumps(ret))
            logging.debug('sent LOCK_UPDATE')
            
        if cmd == CREDS_STORE:
            logging.info('received STORE')

        if cmd == CREDS_COMMIT:
            logging.info('received COMMIT')

        if cmd == CREDS_ABORT:
            logging.info('received ABORT')    

        if cmd == EXT_CLICKED:
            logging.info('received EXT_CLICKED')

        if cmd == NAVIGATE:
            logging.info('received debug NAVIGATE')
            await sock.send(msg)
            logging.info('sent NAVIGATE')

server = websockets.serve(serve, 'localhost', 4000)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
