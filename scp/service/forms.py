# coding: utf-8
from __future__ import unicode_literals
from django import forms
from service.models import TestCase

#from django import newforms as forms



class TestForm(forms.Form):
    test_name = forms.CharField(max_length=50, min_length=1)
    test_file = forms.FileField()
    script_description = forms.CharField(max_length=50, min_length=1)


class UserForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=1)
    password = forms.CharField(max_length=50, min_length=1)
    email = forms.CharField(max_length=50, min_length=1)


JMETER_CHOICES = (
        ('option1', '机器1'),
        ('option2', '机器2'),
        ('option3', '机器3'),
)
attrs_dict = { 'class': 'required' }
class AddScriptForm(forms.Form):
    """
    Form used for adding Snippets.

    """

    #def __init__(self, *args, **kwargs):
        #super(AddScriptForm, self).__init__(*args, **kwargs)
        #self.fields['TestCase'].choices = [('', '----------')] + [(test.id,test.test_name) for test in TestCase.objects.all()]

    test_name = forms.ModelChoiceField(queryset=TestCase.objects.all().values_list('test_name', flat=True),label=u"脚本名称")
    #test_name = forms.ModelChoiceField(queryset=..., to_field_name="name")
    #test_neme = forms.ModelChoiceField(TestCase.object.filter(user=request.user))
    choose_jmeter = forms.ChoiceField(choices=JMETER_CHOICES,label='choose_jmeter')
    #topic = forms.ChoiceField(choices=TOPIC_CHOICES,label='选择评分')
    perform_description = forms.CharField(max_length=200)


