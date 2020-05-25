from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Url

import csv
from django.http import HttpResponse, HttpResponseRedirect

from .serializers import UrlSerializer

class UrlListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UrlSerializer
    queryset = Url.links.all()

# host.com/shortener/{origin_url}

class UrlShortener(APIView):
    def post(self, request, origin_uri):
        try:
            url = Url.links.get(url=origin_uri)
        except:
            url = Url(url=origin_uri)
            url.save()
        short_url = url.short_url
        return Response(short_url)

class UrlView(APIView):
    def get(self, request, hash):
        url = Url.links.get(url_hash=hash)
        url = url.url
        return HttpResponseRedirect(url)

class UrlExport(APIView):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response)
        fields = Url.links.all().values_list('url', 'short_url')
        # writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
        for row in fields:
            writer.writerow(row)
        return response