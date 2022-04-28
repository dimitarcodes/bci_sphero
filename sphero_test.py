import asyncio
from random import randrange
from sphero_mini import SpheroMini


async def init(sphero):
    await sphero.connect()
    await sphero.wake()
    await sphero.getAcknowledgement("wake")
    print('Hello World!')

    await sphero.roll(0,0)
    for _ in range(25):
        await sphero.setLEDColor(red=randrange(255), \
                                    green=randrange(255), blue=randrange(255))
        await sphero.getAcknowledgement("led")

async def do_a_shape(sphero, n_sides):
    turn_angle = int(360/n_sides)
    for i in range(n_sides):
        await sphero.roll(speed=150,heading=(turn_angle*i))
        await asyncio.sleep(1)

async def do_a_shape_corrected(sphero, n_sides):
    turn_angle = int(360/n_sides)
    for i in range(n_sides-1):
        await sphero.roll(speed=150,heading=(turn_angle*i))
        await asyncio.sleep(1)
        if i == n_sides -1:
            await sphero.roll(speed=50, heading = turn_angle*i -180)
            await asyncio.sleep(0.2)

async def disconnect(sphero):
    await sphero.disconnect()
    print('Goodbye World!')

async def disco(sphero):
    for _ in range(25):
        await sphero.setLEDColor(red=randrange(255), \
                                    green=randrange(255), blue=randrange(255))
        await sphero.getAcknowledgement("led")


async def play():
    address = (
        "F7:DF:DC:63:DA:E4"
    )
    # connect to sphero mini
    sphero_mini = SpheroMini(address)
    await init(sphero_mini)

    await do_a_shape(sphero_mini, 4)
    await disco(sphero_mini)
    await do_a_shape_corrected(sphero_mini, 4)
    # close sphero connection
    await disconnect(sphero_mini)

if __name__ == "__main__":
    asyncio.run(play())