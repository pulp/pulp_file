from django.conf.urls import url

from django.http import HttpResponse


def test_root(request):
    return HttpResponse("root test")


def test_named(request):
    return HttpResponse("name test")


def test_nested(request):
    return HttpResponse("nested test")


def test_conflict(request):
    return HttpResponse("confict test")


urlpatterns = [
    url(r'^$', test_root),
    url(r'^test/$', test_named),
    url(r'^plugins/plugin/nested/$', test_nested),
    url(r'^api/v3/status/$', test_conflict),
]
