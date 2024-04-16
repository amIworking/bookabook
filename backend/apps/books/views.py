from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.template.loader import render_to_string
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book
from rest_framework import generics, permissions
from django.db import connection
from .serializers import BookSerializer


@permission_classes((permissions.AllowAny,))
class BookAPIList(generics.ListCreateAPIView):
    queryset = (Book.objects.all()
                    .select_related('author'))
    serializer_class = BookSerializer

@permission_classes((permissions.AllowAny,))
class BookAPIRetrieve(generics.RetrieveUpdateDestroyAPIView):
    queryset = (Book.objects.all()
                    .select_related('author'))
    serializer_class = BookSerializer

