# from django.conf.urls import url
from authorization import views as core_views
from django.urls import path
from .  import views

urlpatterns = [
    # ...
    # url(r'^signup/$', core_views.signup, name='signup'),
    path('', views.signup, name='signup'),

]