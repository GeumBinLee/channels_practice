from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")



def room(request, room_name):
    return render(request,
                  "chat/room.html",
                  {"room_name": room_name}) # 현재 채팅방의 이름을 받아온다.