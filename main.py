#!/usr/bin/env python3

import websockets

import asyncio
import json
import logging
import random
import string

CREDS_SEARCH = 'credentials_search'
CREDS_SUGGEST = 'credentials_suggest'
CREDS_STORE = 'credentials_store'
EXT_CLICKED = 'ext_icon_clicked'
BROWSER_FOCUSED = 'browser_focused'
NAVIGATE = 'navigate'

random_chars = string.ascii_letters + string.digits

logging.basicConfig(level=logging.DEBUG)

def random_string(lower=5, upper=15):
    return ''.join(random.choices(random_chars, k=random.randint(lower, upper)))

async def serve(sock, path):
    logging.info('handling socket %s at path %s', sock, path)
    while True:
        logging.debug('awaiting data')
        msg = await sock.recv()
        logging.debug('received message: %s', msg)

        data = json.loads(msg)
        if 'command' not in data:
            logging.error('no command type found in message')
            continue

        cmd = data['command'].lower()

        if cmd == CREDS_SEARCH:
            logging.info('received SEARCH')
            ret = {
                'command': CREDS_SUGGEST,
                'site': data['site'],
                'credentials': [{
                    'username': random_string(),
                    'password': random_string(),
                }],
                'id': data['id'],
            }

            await sock.send(json.dumps(ret))
            logging.info('sent SUGGEST')

        if cmd == CREDS_STORE:
            logging.info('received STORE')

        if cmd == BROWSER_FOCUSED:
            logging.info('received BROWSER_FOCUS')

        if cmd == EXT_CLICKED:
            logging.info('received EXT_CLICKED')

        if cmd == NAVIGATE:
            logging.info('received debug NAVIGATE')
            await sock.send(msg)
            logging.info('sent NAVIGATE')

server = websockets.serve(serve, 'localhost', 4000)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
