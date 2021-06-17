import argparse
import asyncio
import logging

from time import sleep

from Controller import Controller
from const import buttons, dpad_directions, triggers


class ControllerManagerProtocol:
    def __init__(self):
        self.controller = Controller()
        self.logger = logging.getLogger()
        sleep(1)
        super().__init__()

    def connection_made(self, transport):
        self.logger.info("Connected")
        self.transport = transport

    def connection_lost(self, exc):
        self.logger.info("Connection closed")

    def datagram_received(self, data, addr):
        message = data.decode()
        # invoke controller call
        self.parse_controller_command(message)

    def parse_controller_command(self, message):
        message = message.lower().strip()
        # taps
        if message in buttons.keys():
            self.logger.debug("Pressing {}".format(message))
            self.controller.tap(buttons[message])
        elif message in dpad_directions.keys():
            self.logger.debug("Pressing DPAD {}".format(message))
            self.controller.dpad(dpad_directions[message])
        elif message in triggers:
            self.logger.debug("Pressing trigger {}".format(message))
            self.controller.trigger(message, amount=1)
        else:
            self.logger.warning("Unsupported message: {}".format(message))


async def forever():
    while True:
        await asyncio.sleep(1)


async def main():
    logger = logging.getLogger()
    logger.info("Starting UDP server")

    loop = asyncio.get_event_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ControllerManagerProtocol(), local_addr=("127.0.0.1", 9999)
    )

    try:
        await forever()
    finally:
        transport.close()


if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser("TwitchPlaysDreams Server")
    parser.add_argument(
        "--verbose",
        "-v",
        default=False,
        action="store_true",
        help="Will print more info to the log (i.e. all actions)",
    )
    parser.add_argument(
        "--logfile",
        type=str,
        default="./twitchplays.log",
        action="store",
        help="Set the logfile. Default is twitchplays.log in the current directory",
    )
    args = parser.parse_args()
    # set up logger
    logging.basicConfig(
        filename=args.logfile,
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
        filemode="w",
    )
    logger = logging.getLogger()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error("Uh oh! There was an unexpected error!")
        logger.error(
            "If this happens again, contact VinceKully (Twitter: @VinceKully) or The_Timme"
        )
        logger.error("Copy the following: {}".format(e))
