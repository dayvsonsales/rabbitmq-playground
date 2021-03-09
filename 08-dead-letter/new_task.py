#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

message = ' '.join(sys.argv[1:]) or "Hello World!"

for i in range(0, 5000):
    channel.basic_publish(exchange='',
                        routing_key='task_queue1',
                        body=message + str(i),
    )
print " [x] Sent %r" % (message,)
connection.close()