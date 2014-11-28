# coding: utf-8

from __future__ import unicode_literals
import tempfile

import subprocess
from task.error import TaskError
from django.conf import settings


def run_jmeter(data):
    jmx = tempfile.NamedTemporaryFile("w+b")
    jtl = tempfile.NamedTemporaryFile("w+b")
    jmx.file.write(data.encode('utf-8'))
    jmx.file.flush()

    command = "%s -n -t %s -l %s" % (settings.JMETER_PATH, jmx.name, jtl.name)
    try:
        subprocess.check_call(command, shell=True)
        #subprocess.Popen(command, shell=True)
        print "testing-km"
        jtl.file.seek(0)
        print jtl.file.read
        return jtl.file.read()
    except subprocess.CalledProcessError as e:
        raise TaskError("执行任务失败")
    finally:
        jmx.close()
        jtl.close()

def do(data):
    return run_jmeter(data)


