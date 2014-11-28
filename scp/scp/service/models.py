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
    ]
)

class TestCase(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    name = models.CharField(max_length=50, verbose_name="名字")
    test_data = models.TextField(default="", blank=True, verbose_name="测试数据")
    test_result = models.TextField(default="", blank=True, verbose_name="测试结果")
    status = models.SmallIntegerField(default= TestCaseStatus.NEW, choices=TestCaseStatus.items(), verbose_name="状态")

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = verbose_name_plural = "测试"