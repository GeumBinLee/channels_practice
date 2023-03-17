import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Chat

# async 키워드로 비동기 함수 동작을 알림
# await를 이용해 async 함수를 호출하고 실제 결과값을 받아온다.


# 커넥션 1개 당 consumer 1개가 생성되며, 기본적으로 다른 Consumer와는 데이터를 공유하지 않는다.
# 방에 한 명씩만 밀어넣으면 알람 될 듯?



class ChatConsumer(WebsocketConsumer):
    def connect(self): # 사용자와 웹소켓 연결이 맺어졌을 때 호출
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # 는 Django view의 requeest 객체에서 찾을 수 있는 정보를 가지고 있다.
        # consumers의 메서드 안에서 self.의 형태로 사용한다.
        #  the  is the place to get connection information and
        # where middleware will put attributes it wants to let you access
        # (in the same way that Django’s middleware adds things to request).
        
        
        self.room_group_name = "chat_%s" % self.room_name
        # room_group_nameedms 해당 채널이 속한 그룹의 이름을 정해 준다.


        # Join room group
        async_to_sync(self.channel_layer.group_add)( # 채널을 그룹에 등록한다.
            self.room_group_name,
            self.channel_name
        )

        self.accept() # 연결을 요청한 사용자와 연결을 허용해 주는 함수

    def disconnect(self, close_code): # 사용자와 웹소켓의 연결이 끊겼을 때 호출된다
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)( # 그룹에서의 등록을 해제한다.
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data): # 사용자가 메시지를 보내면 호출된다.
        # username = self.scope["user"].first_name
        # name = self.scope['user'].username
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # message = (username + '(' + name + ')' + ':\n' + message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)( # 실제로 그룹에 속한 모든 채널에 메시지를 보낸다. (그룹당 채널이 한 개면 이거 알람 맞다니까?)
            self.room_group_name, {"type": "chat_message", "message": message}
            # type으로 실제 메시지를 수신했을 때의 이벤트 핸들러를 지정해줄 수 있다.
            # 이번 예제에서는 45번 라인의 chat_message 함수를 핸들러 함수로 지정했다.
        )
        message = Chat.objects.create(content=text_data_json["message"], sender=self.scope['user'])

    # Receive message from room group
    def chat_message(self, event):
        # username = self.scope["user"].username
        message = event["message"]
        # name = self.scope["user"].username

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message,
                                        # "usernamee":username,
                                        # "name":name
                                        }))