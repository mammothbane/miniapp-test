#!/usr/bin/env python3

import websockets

import asyncio
import json
import logging
import random
import string

CREDS_SEARCH = 'credentials_search'
CANDIDATE_CREDS = 'candidate_credentials'
CREDS_STORE = 'credentials_store'
EXT_CLICKED = 'ext_icon_clicked'
BROWSER_FOCUSED = 'browser_focused'

random_chars = string.ascii_letters + string.digits
rand = random.Random()

logging.basicConfig(level=logging.DEBUG)

def random_string(lower=5, upper=15):
    return ''.join(rand.choices(random_chars, k=rand.randint(lower, upper)))

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
                'command': CANDIDATE_CREDS,
                'site': data['site'],
                'credentials': [
                    {'username': random_string(), 'password': random_string()} for _ in range(rand.randint(3, 8))
                ]
            }

            await sock.send(json.dumps(ret))
            logging.info('sent CANDIDATE')

        if cmd == CREDS_STORE:
            logging.info('received STORE')

        if cmd == BROWSER_FOCUSED:
            logging.info('received BROWSER_FOCUS')

        if cmd == EXT_CLICKED:
            logging.info('received EXT_CLICKED')


server = websockets.serve(serve, 'localhost', 4000)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
