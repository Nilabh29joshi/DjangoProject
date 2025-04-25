# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import DeviceLocation
# from asgiref.sync import sync_to_async

# class TrackingConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         device_id = data.get("device_id")
#         latitude = data.get("latitude")
#         longitude = data.get("longitude")

#         if device_id and latitude and longitude:
#             await self.save_location(device_id, latitude, longitude)
#             # You can also broadcast to a group if needed

#     @sync_to_async
#     def save_location(self, device_id, latitude, longitude):
#         DeviceLocation.objects.create(
#             device_id=device_id,
#             latitude=latitude,
#             longitude=longitude
#         )

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Group name is a unique name to broadcast to all clients tracking a device
        self.room_name = "tracking_room"
        self.room_group_name = f"tracking_{self.room_name}"

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive device location message from WebSocket
    async def receive(self, text_data):
        # Text data comes as a string, we parse it
        text_data_json = json.loads(text_data)
        device_id = text_data_json["device_id"]
        latitude = text_data_json["latitude"]
        longitude = text_data_json["longitude"]

        # Send the device location data to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "device_location_update",
                "device_id": device_id,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

    # Receive device location update from the group
    async def device_location_update(self, event):
        device_id = event["device_id"]
        latitude = event["latitude"]
        longitude = event["longitude"]

        # Send the location to WebSocket
        await self.send(text_data=json.dumps({
            "device_id": device_id,
            "latitude": latitude,
            "longitude": longitude,
        }))

        

