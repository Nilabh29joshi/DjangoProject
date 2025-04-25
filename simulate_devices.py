import asyncio
import websockets
import random
import json

# Number of devices to simulate
DEVICE_COUNT = 5

# Server WebSocket URL
WS_URL = "ws://localhost:8000/ws/track/"

# Generate random location near a center point
def random_location(center_lat=28.6139, center_lon=77.2090):
    return {
        "latitude": center_lat + random.uniform(-0.01, 0.01),
        "longitude": center_lon + random.uniform(-0.01, 0.01),
    }

# Simulate a single device
async def simulate_device(device_id):
    try:
        async with websockets.connect(WS_URL) as ws:
            while True:
                loc = random_location()
                message = {
                    "device_id": f"device_{device_id}",
                    "latitude": loc["latitude"],
                    "longitude": loc["longitude"]
                }
                await ws.send(json.dumps(message))
                print(f"[device_{device_id}] Sent: {message}")
                await asyncio.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"[device_{device_id}] Error: {e}")

# Launch multiple device simulations
async def main():
    tasks = [simulate_device(i + 1) for i in range(DEVICE_COUNT)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())