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
from django.urls import path, include
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
router.register(r'books', BookViews.BookShowView, basename='books')
router.register(r'book_change', BookViews.BookChangeView, basename='book_change')
router.register(r'book_review', BookViews.BookReviewShowCreateView,
                basename='book_review')
router.register(r'book_review_change', BookViews.BookReviewChangeView,
                basename='book_review_change')
router.register(r'users', UserViews.UserView,
                basename='users')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
