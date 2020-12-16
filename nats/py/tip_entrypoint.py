import signal
import asyncio
from asyncio.exceptions import TimeoutError
from nats_helper import *



async def TIP_service(loop):

    fe_topic_name = 'frontend'
    tip_topic_name = 'tip'
    nats_url = 'nats://0.0.0.0:4222'
    state = {}
    print('tip service running')

    # 
    # Connect and subscribe
    #
    nc = await open_conn(nats_url)
    await prepare_state(state, [fe_topic_name, tip_topic_name])

    # Subscribe to front end topic and create correct call back.
    await subscribe_to_front_end_topic(nc, fe_topic_name, state)
   
    # Use call back to provide immediate response or nc.request?
    # How to omit response if busy parsing/translating?
    # How to prevent message retrieval such that other tip
    # container can answer the request for parse/translate?
    # Or, reply with busy, then tip fe continues to send out request
    # until a tip container responds with confirmation of "taking
    # the job"?
    # Or, does a single container simply allocate more resources
    # by kicking off additional parse/translate jobs?
    # k8s: How to spin up fixed (max) count of tip containers?

    #
    # Handle sigterm and sigint for ctrl-c and k8s exit 
    #
    def sig_handler():
        print('Caught SIGINT or SIGTERM')
        if nc.is_closed:
            return

        # Unsubscribe and disconnect.
        loop.create_task(close_conn(nc, state))

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), sig_handler)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(TIP_service(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
