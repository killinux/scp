__author__ = 'liminkang'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
def get_mq(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters( '10.121.41.176' ))
    channel = connection.channel()
    channel.queue_declare(queue = 'starttest' )
    print '[*] Waiting for messages. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        print body

    channel.basic_consume(callback, queue = 'starttest' , no_ack = True )
    channel.start_consuming()