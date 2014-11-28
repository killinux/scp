__author__ = 'liminkang'
#!/usr/bin/env python
#coding=utf8
import pika
def send_mq_analysis_result():
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.121.41.176'))
    channel = connection.channel()
    channel.queue_declare(queue = 'start_analysis')
    mq_message = 'start'
    channel.basic_publish(exchange = '', routing_key='start_analysis', body = mq_message)
    print "[x] sent: '" + mq_message + "'\n"
    connection.close()
    return
