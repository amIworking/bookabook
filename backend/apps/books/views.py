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


# Create your views here.
@permission_classes((permissions.AllowAny,))
class BookAPIView(APIView):
    def get(self, request):
        queryset = (Book.objects.all()
                    .select_related('author'))
        return Response({'posts': BookSerializer(queryset, many=True).data})

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_sr = serializer.save()
        if isinstance(book_sr, str):
            return Response({"error": book_sr})
        return Response({"post": book_sr.validated_data}, status=201)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method PUT is not allowed"})
        try:
            book = Book.objects.get(pk=pk)
        except:
            return Response({"error": "A book with given id doesn't exist"})
        serializer = BookSerializer(instance=book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"put": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method DELETE is not allowed"})
        try:
            book = Book.objects.get(pk=pk)
        except:
            return Response({"error": "A book with given id doesn't exist"})
        book.delete()


def index(request):
    data = {"title": 'index'}
    return render(request, 'books/index.html', context=data)


def show_page(request, *args, **kwargs):
    return HttpResponse(f"{kwargs.get("page")}")

def show_book(request, book_name, *args, **kwargs):
    book = get_object_or_404(Book, slug=book_name)
    print(connection)
    return HttpResponse(f"{book.title}, {book.description}")



def get_params(request):
    if request.GET.get('github'):
        return redirect(f'https://github.com/{request.GET['github']}')
    if request.GET.get('page'):
        return redirect('browser_page', page=request.GET['page'])
    if request.GET.get('slug'):
        uri = reverse('book_slug', kwargs={"book_name": request.GET['slug']})
        print(uri)
        return redirect(uri)
def page_not_found(request, exception):
    print("404")
    return HttpResponseNotFound("This page doesn't exist")