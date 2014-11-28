# coding: utf-8

from __future__ import unicode_literals

from django.contrib import admin
from service.models import TestCase


class TestAdmin(admin.ModelAdmin):
    pass
admin.site.register(TestCase, TestAdmin)

