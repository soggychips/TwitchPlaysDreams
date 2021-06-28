import asyncio
import json
from const import buttons, dpad_directions, triggers, sticks
from random import choice, seed, random


class TestClientProtocol:
    def __init__(self, complete):
        self.complete = complete
        self.transport = None

    def connection_made(self, transport):
        print("Connected to server")
        self.transport = transport
        self.send_things()

    def send_single_example(self):
        seed()
        data = {
            "type": None,
            "name": None,
            "amount": None,
            "length": 0 if random() < 0.9 else random(),
        }
        thing = choice(
            [
                ("button", choice(list(buttons.keys()))),
                ("dpad", choice(list(dpad_directions.keys()))),
                ("stick", choice(list(sticks))),
                ("trigger", choice(list(triggers))),
            ]
        )
        data["type"] = thing[0]
        data["name"] = thing[1]
        data["amount"] = (
            [random() * 2 - 1, random() * 2 - 1]
            if data["type"] == "stick"
            else random()
        )
        return data

    def send_combination_example(self):
        seed()
        data = [self.send_single_example() for i in range(5)]
        return data

    def send_things(self):
        seed()
        # Single inputs
        for _ in range(20):
            data = self.send_single_example()
            payload = json.dumps(data)
            print("Sending {}".format(payload))
            self.transport.sendto(payload.encode())
        # Combination Inputs
        for _ in range(5):
            data = self.send_combination_example()
            payload = json.dumps(data)
            print("Sending combination: {}".format(payload))
            self.transport.sendto(payload.encode())
        # Erronous inputs with respect to type
        print("Sending a payload without type")
        data = self.send_single_example()
        del data["type"]
        payload = json.dumps(data)
        self.transport.sendto(payload.encode())
        print("Sending a payload with bad type")
        data = self.send_single_example()
        data["type"] = "garbage"
        payload = json.dumps(data)
        self.transport.sendto(payload.encode())
        # Erronous input for name
        print("Sending a payload with bad name")
        data = self.send_single_example()
        data["name"] = "garbage"
        payload = json.dumps(data)
        self.transport.sendto(payload.encode())
        # Erronous input for amount
        print("Sending a payload with bad amount")
        data = self.send_single_example()
        data["amount"] = "12"
        payload = json.dumps(data)
        self.transport.sendto(payload.encode())
        # OK input for length
        print("Sending a payload with str length")
        data = self.send_single_example()
        data["length"] = "1"
        payload = json.dumps(data)
        self.transport.sendto(payload.encode())
        # Erronous input for length
        print("Sending a payload with bad length")
        data = self.send_single_example()
        data["length"] = "NULL"
        payload = json.dumps(data)
        self.transport.sendto(payload.encode())
        print("Sending a combination payload with a bad length")
        data = self.send_combination_example()
        data[0]["length"] = "NULL"
        payload = json.dumps(data)
        self.transport.sendto(payload.encode())
        # close the connection
        self.transport.close()

    def connection_lost(self, exc):
        print("Connection closed")
        self.complete.set_result(True)


async def main():
    loop = asyncio.get_running_loop()
    complete = loop.create_future()

    transport, _ = await loop.create_datagram_endpoint(
        lambda: TestClientProtocol(complete), remote_addr=("127.0.0.1", 9999)
    )

    try:
        await complete
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
