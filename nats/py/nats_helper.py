import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import json

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

def generic_subscription_cb(state, subject):

    async def _subscription_cb(msg):
        state[subject]['msg'] = msg
        sub = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print('Received a message on {:s}: reply = {:s}, data = {:s}'.format(
            sub, reply, data))

    return _subscription_cb

async def interpret_as_json(raw_data):

    data = None
    try:
        data = json.loads(raw_data)
    except json.decoder.JSONDecodeError as e:
        print('debug:', raw_data)
        data = None

    return data

async def fe_data_cb(msg):

    raw_data = msg.data.decode()
    data = await interpret_as_json(raw_data)

    if data is not None:
        print(data)    

async def nats_conn_err_cb(e):
    print("NATS connection error: {}".format(e))

async def nats_closed_cb():
    await asyncio.sleep(0.1)
    loop = asyncio.get_running_loop()
    loop.stop()

async def prepare_state(state, topics):

    for topic in topics:
        state[topic] = {'sid': None, 'msg': None}

async def subscribe_to_front_end_topic(nc, fe_topic, state):

    sid = await nc.subscribe(fe_topic, cb=fe_data_cb)
    state[fe_topic]['sid'] = sid

    # NATS docs tutorials always flush after subscribing.
    await nc.flush()

#async def open_conn(nats_url, sub_list):

#    # Connect to nats server
#    nc = NATS()
#    await nc.connect(nats_url, no_echo=True, error_cb=nats_conn_err_cb, 
#                     closed_cb=nats_closed_cb)

#    # Subscribe to subjects.
#    subject_sid_dict = {}
#    loop = asyncio.get_running_loop()
#    for subject in sub_list:

#        future = loop.create_future()
#        async def cb(msg):
#            print('Received [{:s}]: {:s}'.format(msg.subject, msg.data.decode()))
#            nonlocal future
#            future.set_result(msg)

#        sid = await nc.subscribe(subject, cb=cb)
#        subject_sid_dict[subject] = {'sid': sid, 'future': future}

#    # NATS docs tutorials always flush after subscribing.
#    await nc.flush()

#    return nc, subject_sid_dict

async def open_conn(nats_url):

    # Connect to nats server
    nc = NATS()
    await nc.connect(nats_url, no_echo=True, error_cb=nats_conn_err_cb, 
                     closed_cb=nats_closed_cb)

    return nc

async def open_conn2(nats_url, sub_list):

    # Connect to nats server
    nc = NATS()
    await nc.connect(nats_url, no_echo=True, error_cb=nats_conn_err_cb, 
                     closed_cb=nats_closed_cb)

    # Subscribe to subjects.
    state = {}
    for subject in sub_list:
        state[subject] = {'sid': None, 'msg': None}
        sid = await nc.subscribe(subject, cb=subscription_cb(state, subject))
        state[subject] = {'sid': sid}

    # NATS docs tutorials always flush after subscribing.
    await nc.flush()

    return nc, state

async def close_conn(nc, state):

    # unsubscribe
    for subject in state.keys():

        if state[subject]['sid'] is not None:
            await nc.unsubscribe(state[subject]['sid'])

    # close
    await nc.close()

#async def request_reply(nc, subject, response):

#    unique_reply_to = new_inbox()
#    await nc.publish_request(subject, unique_reply_to, response)