from django.contrib import admin

from .models import Card, CardGroup

admin.site.site_header = 'FlashCard Admin'
admin.site.site_title = 'FlashCard Admin Area'
admin.site.index_title = 'Welcome to the FlashCard Admin Area'

admin.site.register(Card)
admin.site.register(CardGroup)
