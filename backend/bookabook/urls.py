"""
URL configuration for bookabook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from rest_framework import routers

from apps.books import views as BookViews
from apps.users import views as UserViews
from bookabook import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



router = routers.SimpleRouter()
router.register(r'books', BookViews.BookView, basename='books')
router.register(r'book_reviews', BookViews.BookReviewView,
                basename='book_reviews')
router.register(r'users', UserViews.UserView,
                basename='users')


urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/v1/', include(router.urls)),

]


if settings.DEBUG:
    additional_paths = [path('admin/', admin.site.urls),
                        re_path(r'^auth/', include('djoser.urls')),]
    urlpatterns.extend(additional_paths)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

