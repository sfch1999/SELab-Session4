import datetime
import hashlib
import random
import string

import django
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from seproject.models import User
from django.shortcuts import render
import requests

admin = User()
admin.email, admin.mobile = 'email@email.com', '0000000000'
admin.username, admin.password = 'admin', hashlib.md5('admin'.encode('utf-8')).digest()
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
        if service == 'login':
            return self.login(request.data)
        return HttpResponse('Bad Request', status=400)

    @staticmethod
    def register(data):
        url = 'http://127.0.0.1:8000/api/register'
        response = requests.post(url, data=data)
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def login(data):
        url = 'http://127.0.0.1:8000/api/login'
        response = requests.post(url, data=data)
        return HttpResponse(response.text, status=response.status_code)


class Register(viewsets.ViewSet):
    def handle_request(self, request):
        user = User()
        data = request.data
        try:
            user.email, user.mobile = data['email'], data['mobile']
            user.username, user.password = data['username'], hashlib.md5(data['password'].encode('utf-8')).digest()
            try:
                user.save()
            except django.db.utils.IntegrityError:
                return HttpResponse('Conflict', status=409)
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        return HttpResponse('User created', status=200)


class Login(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            data = request.data
            username, password = data['username'], str(data['password'])
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        user = User.objects.get(username=username)
        print(user.password, hashlib.md5(password.encode('utf-8')).digest())
        if str(user.password) == str(hashlib.md5(password.encode('utf-8')).digest()):
            print(user.token_exp_time)
            print(django.utils.timezone.now())
            if user.token_exp_time > django.utils.timezone.now():
                return HttpResponse(user.token, status=200)
            else:
                user.token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
                user.token_exp_time = django.utils.timezone.now() + django.utils.timezone.timedelta(hours=1, minutes=30)
                user.save()
                return HttpResponse(user.token, status=200)
        else:
            return HttpResponse("Provided Info is wrong!", status=404)
