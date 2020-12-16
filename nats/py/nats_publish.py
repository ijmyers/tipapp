import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import sys
import argparse

async def msg_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print('Received a message on {:s}: reply = {:s}, data = {:s}'.format(
        subject, reply, data))

async def main(nats_url, topic, message):

    # Create NATS client object and connect to server.
    nc = NATS()
    await nc.connect(nats_url, no_echo=True)
        
    await nc.publish(topic, message.encode())

    # Close nats client connection.
    await nc.close()


if __name__ == '__main__':

    #def pair(arg):
    #    return [x for x in arg.split('|')]

    aparse = argparse.ArgumentParser(description='Publish nats message')
    aparse.add_argument('--nats_url', type=str, default='nats://0.0.0.0:4222')
    #aparse.add_argument('-s', '--subscribe', metavar='[subscription n]', type=str, action='append', help='subscription')
    aparse.add_argument('topic', metavar='<Subscription topic>', type=str)
    aparse.add_argument('message', metavar='<message>', type=str)
    
    args = aparse.parse_args()

    asyncio.run(main(args.nats_url, args.topic, args.message), debug=True)
