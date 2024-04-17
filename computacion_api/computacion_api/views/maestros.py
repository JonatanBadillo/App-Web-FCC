from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from computacion_api.serializers import *
from computacion_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json

#Esta funcion permite obtener toda la vista de maestros, mediante el token de autenticacion de inicio de sesion
class MaestrosAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        maestros = Maestros.objects.filter(user__is_active = 1).order_by("id")
        lista = MaestroSerializer(maestros, many=True).data
        
        return Response(lista, 200)

class MaestrosView(generics.CreateAPIView):#Vista que realiza el Post
    #Obtener usuario por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id = request.GET.get("id"))
        maestro = MaestroSerializer(maestro, many=False).data
        maestro["materias_json"] = json.loads(maestro["materias_json"])
        return Response(maestro, 200)
    
    #Registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        user = UserSerializer(data=request.data)
        if user.is_valid():
            #Grab user data
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            #Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()
            #validacion de usuarios para su registro
            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)
            #asignacion de valores a cada campo
            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)

            #Guardar los datos del alumno
            user.set_password(password) #Encripta-cifra la contraseña
            user.save()#Guarda la contraseña cifrada

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            #Create a profile for the maestros
            #Anadir la informacion del maestro creado a el modelo de maestros
            maestro = Maestros.objects.create(user=user,#Aca se liga la FK entre los 2 modelos
                                            id_trabajador= request.data["id_trabajador"],
                                            fecha_nacimiento= request.data["fecha_nacimiento"],
                                            telefono= request.data["telefono"],
                                            rfc= request.data["rfc"].upper(),
                                            cubiculo= request.data["cubiculo"],
                                            area_investigacion= request.data["area_investigacion"],
                                             materias_json = json.dumps(request.data["materias_json"]))#Se usa json.dumps para convertirlo a una cadena de texto JSON y asi poder tratarlo mas facil en la BD
            maestro.save()#Guarda la informacion del maestro

            return Response({"maestro_created_id": maestro.id }, 201)#Si todo sale bien manda un mensaje de 201 (todo correcto)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)#Si hay un error manda un mensaje de 400 (error)
    

    #Se tiene que modificar la parte de edicion y eliminar
class MaestrosViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        # iduser=request.data["id"]
        maestro = get_object_or_404(Maestros, id=request.data["id"])
        maestro.id_trabajador = request.data["id_trabajador"]
        maestro.fecha_nacimiento = request.data["fecha_nacimiento"]
        maestro.telefono = request.data["telefono"]
        maestro.rfc = request.data["rfc"]
        maestro.cubiculo = request.data["cubiculo"]
        maestro.area_investigacion = request.data["area_investigacion"]
        maestro.materias_json = json.dumps(request.data["materias_json"])
        maestro.save()
        temp = maestro.user
        temp.first_name = request.data["first_name"]
        temp.last_name = request.data["last_name"]
        temp.save()
        user = MaestroSerializer(maestro, many=False).data

        return Response(user,200)
    
    #Eliminar maestros
    def delete(self, request, *args, **kwargs):
        profile = get_object_or_404(Maestros, id=request.GET.get("id"))
        try:
            profile.user.delete()
            return Response({"details":"Maestro eliminado"},200)
        except Exception as e:            
            return Response({"details":"No se pudo eliminar el"},200)