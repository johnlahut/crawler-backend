import uuid
from rest_framework import serializers
from .models import Organization, Job

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated') # TODO: This needs to be accurate

class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('id', 'created')

    def create(self, valid_data):

        # create shell of a job, let downstream processes update it
        return  Job.objects.create(
            url=valid_data.get('url'),
            client_id=valid_data.get('client_id'),
            status=Job.NOT_STARTED,
        )
