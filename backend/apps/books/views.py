from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.template.loader import render_to_string
from rest_framework.decorators import permission_classes, action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book, BookReview
from rest_framework import generics, permissions, viewsets, status, mixins
from django.db import connection

from .serializers import (BookSerializerBase, BookChangeSerializer,
                          BookReviewSerializerBase, BookReviewChangeSerializer)
from django_print_sql import print_sql, print_sql_decorator
from .permissions import IsOwnerOrAdminUser, AnyNotAllowed



class BookShowView(viewsets.ReadOnlyModelViewSet):
    queryset = (Book.objects.all()
                    .select_related('author'))
    serializer_class = BookSerializerBase
    lookup_field = 'slug'
    permission_class = (permissions.AllowAny)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        reviews_queryset = BookReview.objects.filter(book_id=response.data['pk'])
        reviews_sr = BookReviewSerializerBase(instance=reviews_queryset, many=True)
        response.data['reviews'] = reviews_sr.data
        return response



class BookChangeView(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = (Book.objects.all()
                    .select_related('author'))
    serializer_class = BookChangeSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.IsAdminUser,)







class BookReviewShowCreateView(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    queryset = (BookReview.objects.all()
                          .select_related('user', 'book'))
    serializer_class = BookReviewSerializerBase
    permission_class = (permissions.IsAuthenticated,)

class BookReviewChangeView(mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                            viewsets.ReadOnlyModelViewSet,):
    permission_classes = (IsOwnerOrAdminUser,)
    queryset = (BookReview.objects.all()
                          .select_related('user', 'book'))
    serializer_class = BookReviewChangeSerializer