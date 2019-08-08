from rest_framework import generics, views, status, permissions
from rest_framework.response import Response

from .models import Organization, Job
from .serializers import OrganizationSerializer, JobSerializer

from uuid import uuid4
# Create your views here.

class StartJobView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer