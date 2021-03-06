import json
import os
from pathlib import Path
import asyncio


if __name__ == "__main__":

    async def run_server_connection(reader, writer):

        credentials = ""
        path = Path("credentials.data")
        if not path.exists():
            path.touch()

        with open("credentials.data", "r") as f:
            data = f.read()
            if data:
                credentials = json.loads(data)
            else:
                credentials = None

        credentials_rpc = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": "3",
                "method": "init_authentication",
                "params": {"stored_credentials": credentials},
            }
        ).encode()

        print('running_browser')
        writer.write(credentials_rpc + b"\n")
        await writer.drain()
        tokens = await reader.readline()
        print("ret", tokens)

        tokens = json.loads(tokens.decode())
        try:
            if 'method' in tokens and tokens['method'] == 'store_credentials':
                with open('credentials.data', 'w') as f:
                    f.write(json.dumps(tokens['params']))

                print("tokens", tokens)
                ret = await reader.readline()
                print("ret", ret)
        except Exception as e:
            print(f'{str(e)}: Removing credentials')
            os.remove('credentials.data')

        print("owned")
        writer.write(b'{"jsonrpc": "2.0", "id": "3", "method": "import_owned_games"}\n')
        await writer.drain()
        ret = await reader.readline()
        print("ret", ret)

        print("local")
        writer.write(b'{"jsonrpc": "2.0", "id": "4", "method": "import_local_games"}\n')
        await writer.drain()
        ret = await reader.readline()
        print("ret", ret)

        # print("install_game")
        # writer.write(b'{"jsonrpc": "2.0", "method": "install_game", "params":{"game_id": "21298"}}\n')

        print("launch_game")
        writer.write(b'{"jsonrpc": "2.0", "method": "launch_game", "params":{"game_id": "1465140039"}}\n')

        # print("uninstall_game")
        # writer.write(b'{"jsonrpc": "2.0", "method": "uninstall_game", "params":{"game_id": "GAME_ID"}}\n')

        # await asyncio.sleep(5)
        # print("shutdown")
        # writer.write(b'{"jsonrpc": "2.0", "id": "6", "method": "shutdown"}\n')

    async def wakeup():
        while True:
            await asyncio.sleep(1)

    async def start_test():
        await asyncio.start_server(run_server_connection, "127.0.0.1", "7998")
        # reader, writer = await asyncio.open_connection("127.0.0.1", "7998")
        # await BNetPlugin(reader, writer, "sdafsdf").run()

    loop = asyncio.get_event_loop()
    loop.create_task(start_test())
    loop.create_task(wakeup())
    loop.run_forever()
