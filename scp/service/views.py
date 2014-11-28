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
from.models import RunJmeter
from models import JmeterStatus
from service.forms import TestForm
from service.forms import AddScriptForm
from task import jmeter
from task import sendmq
from task import sendmq02
from task import getmq
from django import forms
from service.forms import UserForm
from django.contrib.auth.models import User
from multiprocessing import Process, Queue
from django.db.models import Count
from django.template import Template, Context
from django import template



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


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email = form.cleaned_data['email']
            )
            return redirect("/login/")
    else:
        form = UserForm()

    return TemplateResponse(request, "register.html", {"form": form})

@login_required
def test(request):
    tests = TestCase.objects.filter(user=request.user)
    test_name = TestCase.objects.fiter(test_name="test01")
    book = test_name.book_set.all()


    #return render_to_response('test.html', {'tests': tests})
    return TemplateResponse(request,'test.html', {"tests":tests})



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
                test_name=form.cleaned_data['test_name'],
                script_description=form.cleaned_data['script_description'],
                test_data=content,
            )
            #return redirect("/test/")
            tests = TestCase.objects.filter(user=request.user)
            return TemplateResponse(request,'test.html', {'tests': tests})
    else:
        form = TestForm()

    return TemplateResponse(request, "test_add.html", {"form": form})


@login_required
def view_result(request, test_id):
    try:
        tc = TestCase.objects.get(id=test_id)
    except ObjectDoesNotExist as e:
        return TemplateResponse(request, "message.html", {"error_msg": "无效测试"})

    #if tc.status not in [TestCaseStatus.FAILED, TestCaseStatus.SUCCESS]:
    if tc.status not in [TestCaseStatus.FINISH]:
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
        #q = Queue()
        file('E:/1.txt', 'a').write('before process\n')
        p = Process(target=sendmq.send_mq_analysis_result)
        p.start()

        p.join()
        file('E:/1.txt', 'a').write('after process\n')
        #sendmq02.send_mq_analysis_result()
        #sendmq.send_mq_monitor()
        print "mq_message"
        #sendmq02.send_mq_analysis_result()
        tc.test_result = jmeter.do(tc.test_data)
        #sendmq.send_mq_analysis_result()
        tc.status = TestCaseStatus.SUCCESS
        tc.save()


        return TemplateResponse(request, "message.html", {"msg": "执行测试成功！"})
    except Exception as e:
        file('/C/1.txt', 'a').write('exception process %s\n' % str(e))
        tc.status = TestCaseStatus.FAILED
        tc.save()

        return TemplateResponse(request, "message.html", {"error_msg": "执行测试失败"})

def home(request):
    tests = TestCase.objects.filter(user=request.user)

    user_counts = TestCase.objects.filter(user=request.user).count()
    #user_scripts = TestCase.objects.filter()
    return TemplateResponse(request, 'home.html', {"tests": tests ,"user_counts":user_counts })


def index(request):
    return TemplateResponse(request, 'index.html', {})

def all_report(request):
    tests = TestCase.objects.filter(user=request.user)

    return TemplateResponse(request, 'all_report.html', {"tests": tests })
def run(request):

    scripts = TestCase.objects.filter(user=request.user).values_list('test_name', flat=True)
    jmeter_list = JmeterStatus.objects.filter(status = 1).values_list('id', flat=True)
    if request.method == "POST":
        form = AddScriptForm(request.POST)

        if form.is_valid():

            jmeter_list = request.REQUEST.getlist("jmeter_list")
            #perform_description = form.cleaned_data['perform_description']
            test_name = request.getParameter("scripts")
            perform_description = form.cleaned_data['perform_description']
            form1 = TestCase.objects.filter(user=request.user).update(test_name=test_name)
            #form1.save()
            #return TemplateResponse(request, 'temp.html', {"test_name": test_name ,"jmeter_list": jmeter_list})
            return HttpResponseRedirect('/')
    else:

        form = AddScriptForm()
        #return HttpResponseRedirect('/')
        #form = TestForm()


        #if request.POST.has_key('check'):


            #return 0
            #form = AddScriptForm(initial={"username":request.user.username, 'provider':SOURCES_CHOICES[1]})return render_to_response('update_datasource.html', context_instance=RequestContext(request, params))
        #elif request.POST.has_key('submit'):
            #多选jmeter 入库
            #values = request.POST.getlist('select')
            #return 1

    return TemplateResponse(request, 'run.html', {"scripts": scripts ,"jmeter_list": jmeter_list})
def jmeter_list(request):

    list1 = JmeterStatus.objects.filter(status = 1).values_list('id', flat=True)
    return TemplateResponse(request, 'jmeter_list.html', {"list1": list1})
def result(request):
    test_name1 = TestCase.objects.filter(user=request.user)
    test_name = test_name1.objects.filter(do_number=1).values('test_name')
    script_description = TestCase.objects.filter(user=request.user).objects.filter(do_number=1).values('script_description')
    #script_description = script_description.values('script_description')
    #update_time = TestCase.objects.exclude(user=request.user,do_number=1)('update_time')
    #perform_description = TestCase.objects.exclude(user=request.user,do_number=1)('perform_description')
    #list1 = JmeterStatus.objects.filter(status = 1).values_list('id', flat=True)
    return TemplateResponse(request, 'result.html', {"test_name":test_name,"script_description":script_description})

def temp(request):
    jmeter_list = request.REQUEST.getlist("jmeter_list")
    #perform_description = form.cleaned_data['perform_description']
    test_name = request.getParameter("scripts")
    #list1 = JmeterStatus.objects.filter(status = 1).values_list('id', flat=True)
    return TemplateResponse(request, 'temp.html', {"jmeter_list":jmeter_list,"test_name":test_name})