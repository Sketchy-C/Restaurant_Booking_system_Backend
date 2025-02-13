from django.urls import path
from mpesa_stk.views import *

urlpatterns = [
    path('api/stk-push/', stk_push,name='stk-push')
]