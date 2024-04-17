from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.template.loader import render_to_string
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book
from rest_framework import generics, permissions, viewsets
from django.db import connection
from .serializers import BookSerializer

@permission_classes((permissions.AllowAny,))
class BookViewSet(viewsets.ModelViewSet):
    queryset = (Book.objects.all()
                    .select_related('author'))
    serializer_class = BookSerializer
    lookup_field = 'slug'

class BookViewsViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    lookup_field = 'slug'

    #def get_queryset(self):
