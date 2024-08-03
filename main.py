import asyncio
import json
import websockets
import time

TOKEN = "YOUR_DISCORD_USER_TOKEN"

async def keep_online(ws):
    await identify(ws)
    
    while True:
        try:
            await send_heartbeat(ws)
            await asyncio.sleep(heartbeat_interval / 1000.0)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
            await asyncio.sleep(5)
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            await asyncio.sleep(5)
            break

async def identify(ws):
    identify_payload = {
        "op": 2,
        "d": {
            "token": TOKEN,
            "properties": {
                "$os": "linux",
                "$browser": "Termux",
                "$device": "Termux"
            },
            "presence": {
                "status": "online",
                "since": None,
                "afk": False,
                "activities": []
            }
        }
    }
    await ws.send(json.dumps(identify_payload))
    response = await ws.recv()
    data = json.loads(response)
    global heartbeat_interval
    heartbeat_interval = data['d']['heartbeat_interval']
    print(f"Identify response: {response}")

async def send_heartbeat(ws):
    heartbeat_payload = {
        "op": 1,
        "d": int(time.time() * 1000)
    }
    await ws.send(json.dumps(heartbeat_payload))
    response = await ws.recv()
    print(f"Heartbeat response: {response}")

async def main():
    while True:
        try:
            async with websockets.connect('wss://gateway.discord.gg/?v=9&encoding=json') as ws:
                await keep_online(ws)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            await asyncio.sleep(5)

asyncio.run(main())
