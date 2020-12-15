import signal
import asyncio
from asyncio.exceptions import TimeoutError
from nats_helper import *



async def TIP_service(loop):

    config_sub_name = 'config'
    parse_sub_name = 'parse'
    nats_url = 'nats://0.0.0.0:4222'
    print('tip service running')

    # Connect and subscribe.
    nc, state = await open_conn2(nats_url, 
                                            [config_sub_name, parse_sub_name])


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
