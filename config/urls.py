"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include

from core.erp.views.tests.views import TestView, TestClientView
from core.homepage.views import IndexView

from django.conf import settings
from django.conf.urls.static import static

from core.login.views import LoginFormView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('erp/', include('core.erp.urls')),
    path('login/', include('core.login.urls')),
    path('reports/', include('core.reports.urls')),
    # path('', IndexView.as_view(), name='index'),
    path('', LoginFormView.as_view(), name='index'),
    path('test/', TestView.as_view(), name='test'),
    path('testClient/', TestClientView.as_view(), name='testClient'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
