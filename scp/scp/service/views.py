# coding: utf-8

from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (login as auth_login, logout as auth_logout)
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .models import TestCase, TestCaseStatus
from service.forms import TestForm
from task import jmeter


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='login.html'):
    redirect_to = "/"
    next = request.GET.get('next', None)
    if next:
        redirect_to = next

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)

    context = {
        'form': form,
    }

    return TemplateResponse(request, template_name, context)


def logout(request, template_name='logout.html'):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    try:
        auth_logout(request)
        msg = "注销成功!"
    except Exception:
        msg = "注销失败!"

    return TemplateResponse(request, template_name, {'msg': msg})


@login_required
def test(request):
    tests = TestCase.objects.filter(user=request.user)
    return render_to_response('test.html', {'tests': tests})


def handle_uploaded_file(f):
    s = []
    for chunk in f.chunks():
        s.append(chunk.decode('utf-8'))

    return ''.join(s)

@sensitive_post_parameters()
@csrf_protect
@login_required
def add_test(request):
    if request.method == "POST":
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            content = handle_uploaded_file(request.FILES['test_file'])
            TestCase.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                test_data=content,
            )
            return redirect("/test/")
    else:
        form = TestForm()

    return TemplateResponse(request, "test_add.html", {"form": form})


@login_required
def view_result(request, test_id):
    try:
        tc = TestCase.objects.get(id=test_id)
    except ObjectDoesNotExist as e:
        return TemplateResponse(request, "message.html", {"error_msg": "无效测试"})

    if tc.status not in [TestCaseStatus.FAILED, TestCaseStatus.SUCCESS]:
        return TemplateResponse(request, "message.html", {"error_msg": "尚无结果"})


    records = []
    lines = tc.test_result.splitlines()
    for line in lines:
        records.append(line.split(","))

    return TemplateResponse(request, "result.html", {"test": tc, "records": records})


@login_required
def start_test(request, test_id):
    try:
        tc = TestCase.objects.get(id=test_id)
    except ObjectDoesNotExist as e:
        return TemplateResponse(request, "message.html", {"error_msg": "无效测试"})

    if tc.status != TestCaseStatus.NEW:
        return TemplateResponse(request, "message.html", {"error_msg": "新建状态测试才能执行"})

    try:
        tc.status = TestCaseStatus.RUNNING
        tc.save()

        tc.test_result = jmeter.do(tc.test_data)
        tc.status = TestCaseStatus.SUCCESS
        tc.save()

        return TemplateResponse(request, "message.html", {"msg": "执行测试成功！"})
    except Exception as e:
        tc.status = TestCaseStatus.FAILED
        tc.save()

        return TemplateResponse(request, "message.html", {"error_msg": "执行测试失败"})

def home(request):
    return TemplateResponse(request, 'home.html', {})


def index(request):
    return TemplateResponse(request, 'index.html', {})


def tools(request):
    return TemplateResponse(request, 'tools.html', {})
    
    
def contact(request):
    return TemplateResponse(request, 'contact.html', {})


def testing(request):
    return TemplateResponse(request, 'testing.html', {})


def service(request):
    return TemplateResponse(request, 'service.html', {})
