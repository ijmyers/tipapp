import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import sys
import argparse

# async def connect_to_server(nats_client):

#     await nats_client.connect("nats://0.0.0.0:4222")

async def msg_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print('Received a message on {:s}: reply = {:s}, data = {:s}'.format(
        subject, reply, data))

async def main():

    # Create NATS client object and connect to server.
    nc = NATS()
    await nc.connect("nats://0.0.0.0:4222", no_echo=True)
        
    # Subscribe to same channel on which I'll publish.
    sid = await nc.subscribe('foo', cb=msg_handler)

    await nc.publish('foo', b'Hello')
    await nc.publish('foo', b'World')

    # Remove interest in subscription.
    await nc.unsubscribe(sid)

    # Close nats client connection.
    await nc.close()


if __name__ == '__main__':

    
    asyncio.run(main(), debug=True)
