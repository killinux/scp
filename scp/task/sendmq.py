__author__ = 'liminkang'
#!/usr/bin/env python
#coding=utf8
import pika
from multiprocessing import Process, Queue
def send_mq_monitor():

    connection = pika.BlockingConnection(pika.ConnectionParameters('10.121.41.176'))
    channel = connection.channel()
    channel.queue_declare(queue = 'start_monitor')
    mq_message = 'start_monitor_test1111'
    channel.basic_publish(exchange = '', routing_key='start_monitor', body = mq_message)
    print "[x] sent: '" + message + "'\n"
    connection.close()

def send_mq_analysis_result():
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.121.41.176'))
    channel = connection.channel()
    channel.queue_declare(queue = 'start_analysis')
    mq_message = 'start'
    channel.basic_publish(exchange = '', routing_key='start_analysis', body = mq_message)
    print "[x] sent: '" + message + "'\n"
    connection.close()



