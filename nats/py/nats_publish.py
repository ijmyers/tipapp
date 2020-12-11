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

async def main(nats_url, message):

    # Create NATS client object and connect to server.
    nc = NATS()
    await nc.connect(nats_url, no_echo=True)
        
    # Subscribe to same channel on which I'll publish.
    #sid = await nc.subscribe('foo', cb=msg_handler)
    for msg_pair in message:
        await nc.publish(msg_pair[0], msg_pair[1].encode())
    #await nc.publish('foo', b'World')

    # Remove interest in subscription.


    # Close nats client connection.
    await nc.close()


if __name__ == '__main__':

    def pair(arg):
        return [x for x in arg.split(',')]

    aparse = argparse.ArgumentParser(description='Publish nats message')
    aparse.add_argument('--nats_url', type=str, default='nats://0.0.0.0:4222')
    aparse.add_argument('-s', '--subscribe', metavar='[subscription n]', type=str, action='append', help='subscription')
    aparse.add_argument('-m', '--message', type=pair, default=None, action='append')
    args = aparse.parse_args()

    print(args.message)
    asyncio.run(main(args.nats_url, args.message), debug=True)
