from django.shortcuts import render

def index(request) :
    return render(request, 'notification/index.html')
