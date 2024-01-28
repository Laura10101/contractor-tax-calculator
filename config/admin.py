from django.contrib import admin
from django.urls import path
from .views import config

# Register your models here.
class ConfigAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        urls += [path("config/", self.admin_site.admin_view(config))]
        return urls