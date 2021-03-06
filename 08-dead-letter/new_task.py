#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.queue_declare(queue='task_queue1',
  arguments={
  "x-dead-letter-exchange" : "dlx",
  "x-dead-letter-routing-key" : "dl",
}
)

for i in range(0, 100000):
    channel.basic_publish(exchange='',
                        routing_key='task_queue1',
                        body=message + str(i),
    )
print " [x] Sent %r" % (message,)
connection.close()