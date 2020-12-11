import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def msg_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print('Received a message on {:s}: reply = {:s}, data = {:s}'.format(
        subject, reply, data))

async def main():

    nc = NATS()
    await nc.connect("nats://0.0.0.0:4222", no_echo=True)

    sid = await nc.subscribe('foo', cb=msg_handler)

    try:
        response = await nc.request('foo', b'my response', timeout=30)
        print('[response]', response.data.decode())
    except ErrTimeout:
        print('Request timed out')

    await nc.unsubscribe(sid)
    await nc.close()

if __name__ == '__main__':

    asyncio.run(main(), debug=True)
