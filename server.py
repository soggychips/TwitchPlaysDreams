import asyncio
from Controller import Controller
from const import buttons, dpad_directions, triggers
from time import sleep

class ControllerManagerProtocol:

    def __init__(self):
        self.controller = Controller()
        sleep(1)
        super().__init__()
        
    def connection_made(self, transport):
        print("Connected")
        self.transport = transport

    def connection_lost(self, exc):
        print("Connection closed")

    def datagram_received(self, data, addr):
        message = data.decode()
        # invoke controller call
        self.parse_controller_command(message)

    def parse_controller_command(self, message):
        message = message.lower().strip()
        # taps
        if message in buttons.keys():
            print("Pressing {}".format(message))
            self.controller.tap(message)
        elif message in dpad_directions.keys():
            print("Pressing DPAD {}".format(message))
            self.controller.dpad(message)
        elif message in triggers:
            print("Pressing trigger {}".format(message))
            self.controller.trigger(message, amount=1)
        else:
            print("Unsupported message: {}".format(message))
        
async def forever():
    while True:
        await asyncio.sleep(1)

async def main():
    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_event_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ControllerManagerProtocol(),
        local_addr=('127.0.0.1', 9999))

    try:
        await forever()
    finally:
        transport.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Uh oh! There was an unexpected error!")
        print("If this happens again, contact VinceKully (Twitter: @VinceKully) or The_Timme")
        print("Copy the following: {}".format(e))