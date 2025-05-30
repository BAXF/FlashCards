from django.db import models
import uuid
from django.urls import reverse

    
class CardGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    image = models.ImageField(upload_to='card_groups/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Card(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    group = models.ForeignKey('CardGroup', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='cards/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.DRAFT)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
