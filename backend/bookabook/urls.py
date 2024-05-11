from django.conf.urls.static import static

from django.contrib import admin

from django.urls import path, include, re_path

from rest_framework import routers

from apps.books import views as BookViews

from apps.users import views as UserViews

from bookabook import settings


router = routers.SimpleRouter()
router.register(r'books', BookViews.BookView, basename='books')
router.register(r'book_reviews', BookViews.BookReviewView,
                basename='book_reviews')
router.register(r'authors', BookViews.AuthorView,
                basename='authors')
router.register(r'users', UserViews.UserView,
                basename='users')

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls'),),
    re_path(r'^auth/', include('djoser.urls.jwt'),),
    path(r'verify_email/<str:token>/',
         UserViews.UserView.as_view({'get': 'verify_email'})),

    path('api/v1/', include(router.urls)),
]


if settings.DEBUG:
    additional_paths = [path('admin/', admin.site.urls),]
    urlpatterns.extend(additional_paths)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
