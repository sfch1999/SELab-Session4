import django
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from seproject.models import User
from django.shortcuts import render
import requests

admin = User()
admin.email, admin.mobile = 'email@email.com', '0000000000'
admin.username, admin.password = 'admin', str(hash('admin'))
admin.isAdmin = True
try:
    admin.save()
except django.db.utils.IntegrityError:
    admin = User.objects.get(username='admin')


class API(viewsets.ViewSet):
    def handle_request(self, request):
        print(request.data)
        try:
            service = request.data["service"]
        except KeyError:
            return HttpResponse('Bad Request', status=400)
        if service == 'register':
            return self.register(request.data)
        return HttpResponse('Bad Request', status=400)

    @staticmethod
    def register(data):
        url = 'http://127.0.0.1:8000/api/register'
        response = requests.post(url, data=data)
        return HttpResponse(response.text,status=response.status_code)


class Register(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            data = request.data
            user = User()
            user.email, user.mobile = data['email'], data['mobile']
            user.username, user.password = data['username'], str(hash(data['password']))
            user.save()
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        except django.db.utils.IntegrityError:
            return HttpResponse('Conflict', status=409)
        return HttpResponse('User created',status=200)
