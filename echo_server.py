import asyncio

""" Use this to print out what your client sends """

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        print("Connection closed")

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))


async def main():
    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('127.0.0.1', 9999))

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass