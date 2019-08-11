from urllib.parse import urlparse

from scrapyd_api import ScrapydAPI
from django.conf import settings
from rest_framework import views, status, viewsets
from rest_framework.response import Response

from .serializers import JobSerializer
from .models import Job

scrapyd = ScrapydAPI(settings.SCRAPYD_API)

class StartJobView(views.APIView):
    def post(self, request):

        # map incoming 'id' field to 'client_id'
        request.data['client_id'] = request.data['id']
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():

            # create job entry
            serializer.save()
            id = serializer.data.get('id')
            url = serializer.data.get('url')
            domain = urlparse(url).netloc


            # get pk to pass to spider
            settings = {
                'id': id,
            }

            # schedule job, update job model with scrapy_id
            task_id = scrapyd.schedule('default', 'orgspider', settings=settings, url=url, domain=domain)
            Job.objects.filter(id=id).update(task_id=task_id)

            # re-serialize; needed to update job with scrapy_id
            serializer = JobSerializer(Job.objects.get(id=id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatusView(viewsets.ReadOnlyModelViewSet):

    serializer_class = JobSerializer
    lookup_field = 'client_id'
    lookup_url_kwarg = 'ids'

    def get_queryset(self):
        return Job.objects.filter(client_id__in=self.request.data.get('ids'))
