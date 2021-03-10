#!/usr/bin/env python
import pika
import time
import random
from datetime import datetime
from datetime import timedelta  

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='supervisor',
  arguments={
  "x-dead-letter-exchange" : "dlx",
  "x-dead-letter-routing-key" : "dl",
}
)

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    print " Verifying if header contains custom-expire property"

    if properties.headers is None:
        properties.headers = dict()

        properties.headers["x-custom-delay"] = 30
        properties.headers["x-custom-expire"] = datetime.now() + timedelta(seconds=properties.headers["x-custom-delay"])
        properties.headers["x-custom-retry"] = 3

        ch.basic_publish(exchange='',
                      routing_key='task_queue1',
                      properties=properties,
                      body=body)

        ch.basic_ack(delivery_tag = method.delivery_tag)
    else:
        if ("x-custom-delay" not in properties.headers) or ("x-custom-expire" not in properties.headers) or ("x-custom-retry" not in properties.headers):
            properties.headers["x-custom-delay"] = 30
            properties.headers["x-custom-expire"] = datetime.now() + timedelta(seconds=properties.headers["x-custom-delay"])
            properties.headers["x-custom-retry"] = 3

            ch.basic_publish(exchange='',
                        routing_key='task_queue1',
                        properties=properties,
                        body=body)

            ch.basic_ack(delivery_tag = method.delivery_tag)
        else:
            if properties.headers["x-custom-retry"] <= 1:
                print "No more retries"
                ch.basic_ack(delivery_tag = method.delivery_tag)
            elif datetime.now() >= properties.headers["x-custom-expire"]:
                properties.headers["x-custom-delay"] *= 2
                properties.headers["x-custom-expire"] = datetime.now() + timedelta(seconds=properties.headers["x-custom-delay"])
                properties.headers["x-custom-retry"] -= 1

                ch.basic_publish(exchange='',
                    routing_key='task_queue1',
                    properties=properties,
                    body=body)

                ch.basic_ack(delivery_tag = method.delivery_tag)
            else:
                ch.basic_reject(delivery_tag = method.delivery_tag)

channel.basic_consume(queue='supervisor', on_message_callback=callback)

channel.start_consuming()