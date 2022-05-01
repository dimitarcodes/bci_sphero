import asyncio

from random import randrange
from sphero_mini import SpheroMini
import socket

async def run():
    # mac address of sphero mini
    address = (
        "F7:DF:DC:63:DA:E4"
    )

    host = 'localhost'  # Server ip - sphero controller should be connected to wifi broadcast of unicorn controller
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    # connect to sphero mini
    my_sphero = SpheroMini(address)
    try:
        await my_sphero.connect()

        # wake sphero
        await my_sphero.wake()
        await my_sphero.getAcknowledgement("wake")

        for _ in range(50):
            await my_sphero.setLEDColor(red=randrange(255), \
                green=randrange(255),blue=randrange(255))
            await my_sphero.getAcknowledgement("led")

        while True:
            data, addr = s.recvfrom(1024)
            data = data.decode('utf-8')
            if data == '0':
                await my_sphero.setLEDColor(red=255, green=0, blue = 0)
                await my_sphero.roll(speed=150,heading=0)
                await asyncio.sleep(1)

                # #resting
                # for _ in range(50):
                #     await my_sphero.setLEDColor(red=randrange(255), \
                #         green=randrange(255),blue=randrange(255))
                #     await my_sphero.getAcknowledgement("led")
            if data == '1':
                # left
                await my_sphero.setLEDColor(red=0, green=0, blue=255)
                #await my_sphero.roll(speed=150, heading = 270)
                await asyncio.sleep(1)
                # await my_sphero.setLEDColor(red=255, green=0, blue = 0)
                await my_sphero.roll(speed=150,heading=180)
                # await asyncio.sleep(1)
            if data == '2':
                # right hand
                await my_sphero.setLEDColor(red=0, green = 255, blue = 0)
                await my_sphero.roll(speed=150, heading=90)
                await asyncio.sleep(1)
            if data == '3':
                # feet
                await my_sphero.setLEDColor(red=0, green=0, blue=255)
                await my_sphero.roll(speed=150, heading = 270)
                await asyncio.sleep(1)

    finally:
        await my_sphero.disconnect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    #loop.set_debug(True)
    loop.run_until_complete(run())
