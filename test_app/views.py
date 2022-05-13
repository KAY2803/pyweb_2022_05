from datetime import datetime
import random

from django.views import View
from django.http import HttpRequest, HttpResponse


class DatetimeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        now = datetime.now()
        return HttpResponse(now)


class RandomNumView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        rnum = random.randint(1, 1000000000)
        return HttpResponse(rnum)
