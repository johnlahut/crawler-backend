from django.db import models
from jsonfield import JSONField

import uuid

# Create your models here.

class Job(models.Model):

    # TODO: This should be a constant
    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    ERROR = 'error'
    WARNING = 'warning'
    COMPLETE = 'completed'
    
    STATUSES = (
        (NOT_STARTED, NOT_STARTED),
        (IN_PROGRESS, IN_PROGRESS),
        (ERROR, ERROR),
        (WARNING, WARNING),
        (COMPLETE, COMPLETE),
    )


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    client_id = models.UUIDField(default=uuid.uuid4(), unique=True)
    task_id = models.UUIDField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=NOT_STARTED)
    url = models.CharField(max_length=255)
    crawled_data = JSONField(null=True)

    def __str__(self):
        return f'{self.id} {self.url}'

class Organization(models.Model):

    """
    TODO: CharFields are currently used for temp purposes. Should restrict these down to more accurate types
    TODO: Database will most likely which allows for array type columns. Use this for the many list like structures
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    review_date = models.DateTimeField(blank=True)
    url = models.URLField(blank=True)
    status = models.CharField(max_length=255, blank=True)

    name = models.CharField(max_length=255, blank=True)
    mission = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    geo_area = models.CharField(max_length=255, blank=True)
    locations = models.CharField(max_length=255, blank=True)

    keywords = models.CharField(max_length=255, blank=True)
    aliases = models.CharField(max_length=255, blank=True)
    languages = models.CharField(max_length=255, blank=True)
    ein = models.PositiveIntegerField()

    # TODO: This should be its own model
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)


    def __str__(self):
        return f'{self.id} {self.url}'