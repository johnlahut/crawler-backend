from rest_framework import serializers
from .models import Organization, Job

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated') # TODO: This needs to be accurate

class JobSerializer(serializers.ModelSerializer):

    # map incoming 'id' JSON key to its correct client_id field
    id = serializers.UUIDField(source='client_id')

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('id', 'created')

    def create(self, valid_data):

        # call crawler processor here

        return  Job.objects.create(
            url=valid_data.get('url'),
            client_id=valid_data.get('client_id'),
            status='in_progress'
        )
