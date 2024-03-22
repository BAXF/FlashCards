from django.db import models
import uuid
from django.urls import reverse

class Card(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'

    class LEVEL_CHOICES(models.TextChoices):
        EASY = 'easy', 'Easy'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES.choices, default=LEVEL_CHOICES.EASY)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.DRAFT)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
