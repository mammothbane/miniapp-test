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

random_chars = string.ascii_letters + string.digits
rand = random.Random()

logging.basicConfig(level=logging.DEBUG)

def random_string(lower=5, upper=15):
    return ''.join(rand.choices(random_chars, k=rand.randint(lower, upper)))

async def serve(sock, path):
    logging.info('handling socket %s at path %s', sock, path)
    logging.debug('awaiting data')
    msg = await sock.recv()
    logging.debug('received message: %s', msg)

    msg = json.loads(msg)
    if 'command' not in msg:
        logging.error('no command type found in message')
        return

    if 'site' not in msg:
        logging.error('site not found in message')
        return

    cmd = msg['command'].lower()

    if cmd == CREDS_SEARCH:
        logging.debug('received SEARCH')
        ret = {
            'command': CANDIDATE_CREDS,
            'site': msg['site'],
            'credentials': [
                {'username': random_string(), 'password': random_string()} for _ in range(rand.randint(3, 8))
            ]
        }

        await sock.send(json.dumps(ret))
        loging.info('sent CANDIDATE')

    if cmd == CREDS_STORE:
        logging.info('received STORE')
        pass


server = websockets.serve(serve, 'localhost', 4000)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
