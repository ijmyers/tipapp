import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

# To be used on sending side to request reponse on a certain subject.
# Supposedly automatically generates a unique inbox to the reciever
# to reply to: https://docs.nats.io/developing-with-nats/sending/request_reply
async def request_msg(nc, sub, response, timeout):

    try:
        response = await nc.request(sub, response, timeout=timeout)
        print('[response]', response.data.decode())
    except asyncio.TimeoutError:
        print('Request timed out')

async def msg_handler(msg):

    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print('Received a message on {:s}: reply = {:s}, data = {:s}'.format(
        subject, reply, data))

#async def sub_callback(msg):

#    nonlocal future
#    future.set_result(msg)

async def open_conn(nats_url, sub_list):

    # Connect to nats server
    nc = NATS()
    await nc.connect(nats_url, no_echo=True)

    # Subscribe to subjects.
    subject_sid_dict = {}
    loop = asyncio.get_running_loop()
    for subject in sub_list:

        future = loop.create_future()
        async def cb(msg):
            print('Received [{:s}]: {:s}'.format(msg.subject, msg.data.decode()))
            nonlocal future
            future.set_result(msg)

        sid = await nc.subscribe(subject, cb=cb)
        subject_sid_dict[subject] = {'sid': sid, 'future': future}

    # NATS docs tutorials always flush after subscribing.
    await nc.flush()

    return nc, subject_sid_dict

async def close_conn(nc, subject_sid_dict):

    # unsubscribe
    for subject, subjdict in subject_sid_dict.items():
        #print('Unsubscribing from \'{:s}\', sid = {:d}'.format(
        #    subject, subjdict['sid']))

        # Gracefully unsubscribe: get in-flight and cached and
        # halt other messages. 
        # Note: drain causes an error. not sure why or how to solve it.
        #await nc.drain(subjdict['sid'])
        await nc.unsubscribe(subjdict['sid'])

    await nc.close()

#async def request_reply(nc, subject, response):

#    unique_reply_to = new_inbox()
#    await nc.publish_request(subject, unique_reply_to, response)