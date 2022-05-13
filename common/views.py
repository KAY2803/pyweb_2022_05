from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render


class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        # h = """<h1>Hello, World</h1>"""
        return HttpResponse('Hello, World')


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "common/index.html")