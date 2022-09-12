"""test_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('auth/', include('authorization.urls')),
    # path('')
    path("api/", api.urls),
]
"""
Функция include() позволяет ссылаться на другие конфигурации URL. Всякий раз, когда Django встречает include(),
 он отсекает любую часть URL-адреса, совпадающую с этой точкой, и отправляет оставшуюся строку во включенную конфигурацию
  URL для дальнейшей обработки.

Идея include() состоит в том, чтобы упростить подключение
 URL-адресов по принципу plug-and-play.
  Поскольку опросы находятся в собственной конфигурации 
  URL (polls/urls.py), их можно разместить в «/polls/», или в «/fun_polls/», 
  или в «/content/polls/», или в любой другой корень пути, 
  и приложение по-прежнему будет работать.
"""