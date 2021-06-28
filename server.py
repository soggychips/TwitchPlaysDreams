import argparse
import asyncio
import logging
import json
from time import sleep
from Controller import Controller


class ControllerManagerProtocol:
    def __init__(self):
        self.controller = Controller()
        self.logger = logging.getLogger()
        sleep(1)
        self.type_map = {
            "button": self.controller.button,
            "dpad": self.controller.dpad,
            "stick": self.controller.stick,
            "trigger": self.controller.trigger,
            None: lambda *_: self.logger.warning(
                "type must be provided - message thrown out"
            ),
        }
        super().__init__()

    def connection_made(self, transport):
        self.logger.info("Connected")
        self.transport = transport

    def connection_lost(self, _):
        self.logger.info("Connection closed")

    def datagram_received(self, data, _):
        try:
            message = data.decode()
            message = json.loads(message)
            self.logger.debug("Message received: {}".format(message))
        except Exception as e:
            raise e
        try:
            # invoke controller call
            self.parse_controller_command(message)
        except Exception as e:
            self.logger.error("Error in datagram_received: {}".format(e))

    def parse_controller_command(self, data):
        # determine input type
        if isinstance(data, dict):
            # single input
            self.controller.single(
                func=self.type_map.get(
                    data.get("type"),
                    lambda *_: logger.warning(
                        "'{}' is not a supported type".format(data["type"])
                    ),
                ),
                **data
            )
        elif isinstance(data, list):
            # combination input
            funcs = [
                self.type_map.get(
                    msg.get("type"),
                    lambda *_: logger.warning(
                        "'{}' is not a supported type".format(data["type"])
                    ),
                )
                for msg in data
            ]
            self.controller.combination(funcs, data)
        else:
            self.logger.warning("Unsupported message format: {}".format(type(data)))


async def forever():
    while True:
        await asyncio.sleep(1)


async def main():
    logger = logging.getLogger()
    logger.info("Starting UDP server")

    loop = asyncio.get_event_loop()

    transport, _ = await loop.create_datagram_endpoint(
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
