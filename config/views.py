"""Define views for the config app."""

from django.shortcuts import render
from django.contrib import admin


@admin.site.admin_view
def config(request):
    """Display the config app template."""
    """This is a single page application so"""
    """this view only needs to render the template"""
    template = 'config/config.html'
    return render(request, template)
