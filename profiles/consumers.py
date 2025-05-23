import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
from django.utils.formats import date_format
from profiles.models import UserProfile
from community.models import CommunityMessage

'''
Used Chat-GPT
'''


class ProfileDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = "community"  # Common room for everyone

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(
            f"User {self.user.username if self.user.is_authenticated else 'Anonymous'} "
            "connected to community"
        )

    async def disconnect(self, close_code):
        # Leaving the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(
            f"User {self.user.username if self.user.is_authenticated else 'Anonymous'} "
            f"disconnected from community with code: {close_code}"
        )

    # Receiving a message from WebSocket (from profile page)
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            user = self.scope["user"]

            try:
                profile = await UserProfile.objects.aget(user=user)
            except UserProfile.DoesNotExist:
                profile = None

            now = date_format(timezone.now(), "N j, Y, P")
            day_name = timezone.now().strftime("%A")  # Get the full day name

            # Forming a message for broadcasting to the community
            community_message = {
                "user": (
                    profile.nickname
                    if profile and profile.nickname
                    else user.username
                ) if user.is_authenticated else "Anonymous",
                "message": (
                    f"The goal '{data.get('content_item', '')}' "
                    f"in plan '{data.get('plan_name', '')}' "
                    f"for week {data.get('week_number', '')} "
                    f"(on {day_name}) was {data.get('status', '')}"
                ),

                "timestamp": now,
                "avatar": data.get('avatar', '/media/avatars/default_avatar.jpg')
            }

            # Save massage to db
            # Save the message asynchronously
            await sync_to_async(CommunityMessage.objects.create)(
                user=community_message["user"],
                message=community_message["message"],
                avatar=community_message["avatar"],
                timestamp=community_message["timestamp"]
            )

            # Sending a message to everyone in a community group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'community.message',  # Event type
                    'user': community_message['user'],
                    'message': community_message['message'],
                    'timestamp': community_message['timestamp'],
                    'avatar': community_message['avatar'],
                }
            )

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)

    """
    Event handler for community message (send back to WebSocket Community page)
    """
    async def community_message(self, event):
        user = event['user']
        message = event['message']
        timestamp = event['timestamp']
        avatar = event['avatar']

        # Sending a message back to WebSocket (to the Community page)
        await self.send(text_data=json.dumps({
            'user': user,
            'message': message,
            'timestamp': timestamp,
            'avatar': avatar,
        }))
