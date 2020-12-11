import asyncio
from asyncio.exceptions import TimeoutError
from nats_helper import *

async def TIP_service():

    config_sub_name = 'config'
    parse_sub_name = 'parse'
    nats_url = 'nats://0.0.0.0:4222'
    complete = False

    while not complete:

        print('tip service running')

        # Connect and subscribe.
        nc, subject_sid_dict = await open_conn(nats_url, 
                                               [config_sub_name, parse_sub_name])
        await asyncio.sleep(2.0)

        print('waiting for first incoming message')
        # Wait for msg published on config_sub_name. No need
        # to do other work until that happens.
        try:
            msg = await asyncio.wait_for(
                subject_sid_dict[config_sub_name]['future'], 30)
        except TimeoutError as e:
            #future = subject_sid_dict[config_sub_name]['future']
            #if future.cancel():
            #    print("Future exception: {}".format(future.exception()))
            print('Timed out: {}'.format(e))

        # Unsubscribe and disconnect.
        await close_conn(nc, subject_sid_dict)
        print('tip service done')
        complete = True


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(TIP_service())
    finally:

        # stop for loop.run_forever()
        #loop.stop()
        loop.close()
