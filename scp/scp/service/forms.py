# coding: utf-8

from __future__ import unicode_literals

from django import forms
from service.models import TestCase


class TestForm(forms.Form):
    name = forms.CharField(max_length=50, min_length=1)
    test_file = forms.FileField()