# coding: utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from service.util import EntityState


TestCaseStatus = EntityState(
    [
        [0, "NEW", "新建"],
        [1, "RUNNING", "执行中"],
        [2, "SUCCESS", "成功"],
        [3, "FAILED", "失败"],
        [4, "FINISH","完成"],
    ]
)

class TestCase(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    test_name = models.CharField(max_length=50, unique= True,verbose_name="测试用例名")
    test_data = models.TextField(default="", blank=True, verbose_name="测试数据")
    #test_result = models.TextField(default="", blank=True, verbose_name="测试结果")
    #status = models.SmallIntegerField(default= TestCaseStatus.NEW, choices=TestCaseStatus.items(), verbose_name="状态")
    create_time = models.DateTimeField(verbose_name="create_time",auto_now_add=True)
    #update_time = models.DateTimeField(verbose_name="update_time",auto_now=True)
    script_description = models.CharField(max_length=50, verbose_name="脚本说明")
    #perform_description = models.CharField(max_length=50, verbose_name="执行说明")
    #result_time = models.DateTimeField(verbose_name="result_time",auto_now=True)
    #jmeter_list = models.CharField(max_length=50,verbose_name="执行jmeter列表")
    #do_number = models.IntegerField()


    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = verbose_name_plural = "测试"

class JmeterStatus(models.Model):
    ip = models.CharField(max_length=50, verbose_name="jmeter_ip")
    status = models.CharField(max_length=50, verbose_name="jmeter_status")

class RunJmeter(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    test_name = models.ForeignKey(TestCase, related_name='test_name_runjmeter')
    perform_description = models.CharField(max_length=50, verbose_name="执行说明")
    status = models.SmallIntegerField(default= TestCaseStatus.NEW, choices=TestCaseStatus.items(), verbose_name="状态")
    test_result = models.TextField(default="", blank=True, verbose_name="测试结果")
    jmeter_list = models.CharField(max_length=50,verbose_name="执行jmeter列表")
    update_time = models.DateTimeField(verbose_name="update_time",auto_now=True)
    result_time = models.DateTimeField(verbose_name="result_time")
    do_number = models.IntegerField()




















