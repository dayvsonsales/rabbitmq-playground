#!/usr/bin/env python
import pika
import time
import random

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue1',
  arguments={
  "x-dead-letter-exchange" : "dlx",
  "x-dead-letter-routing-key" : "dl",
}
)
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    print properties

    ch.basic_reject(delivery_tag = method.delivery_tag, requeue=False)
    

channel.basic_consume(queue='task_queue1', on_message_callback=callback)

channel.start_consuming()

