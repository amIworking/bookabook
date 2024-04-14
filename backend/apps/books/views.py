from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Author, Book


# Create your views here.

def index(request):
    data = {"title": 'index'}
    return render(request, 'books/index.html', context=data)


def show_page(request, *args, **kwargs):
    return HttpResponse(f"{kwargs.get("page")}")

def show_book(request, book_name, *args, **kwargs):
    book = get_object_or_404(Book, slug=book_name)
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