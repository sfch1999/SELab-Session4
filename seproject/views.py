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

failed_atts = [0, 0, 0]


class API(viewsets.ViewSet):
    def handle_request(self, request):
        print(request.data)
        try:
            service = request.data["service"]
        except KeyError:
            return HttpResponse('Bad Request', status=400)
        if service == 'register':
            if failed_atts[0] < 3:
                return self.register(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'login':
            if failed_atts[1] < 3:
                return self.login(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)

        if service == 'profile':
            if failed_atts[2] < 3:
                return self.profile(request.data)
            else:
                return HttpResponse('Service Unavailable', status=503)
        return HttpResponse('Bad Request', status=400)

    @staticmethod
    def register(data):
        url = 'http://127.0.0.1:8000/api/register'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[0] += 1
            return HttpResponse('Service Unavailable', status=503)
        if response.status_code/100==5:
            failed_atts[0] += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def login(data):
        url = 'http://127.0.0.1:8000/api/login'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)
        if response.status_code/100==5:
            failed_atts[1] += 1
            return HttpResponse('Service Unavailable', status=503)
        return HttpResponse(response.text, status=response.status_code)

    @staticmethod
    def profile(data):
        url = 'http://127.0.0.1:8000/api/profile'
        try:
            response = requests.post(url, data=data, timeout=0.500)
        except:
            failed_atts[2] += 1
            return HttpResponse('Service Unavailable', status=503)
        if response.status_code/100==5:
            failed_atts[2] += 1
            return HttpResponse('Service Unavailable', status=503)
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
            username, password = request.data['username'], str(request.data['password'])
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)
        user = User.objects.get(username=username)
        if str(user.password) == str(hashlib.md5(password.encode('utf-8')).digest()):
            if user.token_exp_time > django.utils.timezone.now():
                return HttpResponse(user.token, status=200)
            else:
                user.token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
                user.token_exp_time = django.utils.timezone.now() + django.utils.timezone.timedelta(hours=1, minutes=30)
                user.save()
                return HttpResponse(user.token, status=200)
        else:
            return HttpResponse("Provided Info is wrong!", status=404)


class Profile(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            token = request.data['token']
        except KeyError:
            return HttpResponse('Required fields are empty!!!', status=406)

        user = User.objects.get(token=token)
        if not user:
            return HttpResponse('Token not valid', status=409)

        if user.token_exp_time < django.utils.timezone.now():
            return HttpResponse('Token expired', status=409)

        if 'profile' in request.data:
            user.profile = request.data['profile']
            user.save()

        return HttpResponse('your profile: ' + user.profile, status=200)
