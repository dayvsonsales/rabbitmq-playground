#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

consumer_tag = ""

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback2(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    channel.basic_ack(delivery_tag=method.delivery_tag)

def callback(ch, method, properties, body):
    global consumer_tag

    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    channel.basic_cancel(consumer_tag)

    print(" [x] Done")
    print(" [x] Restart")

    consumer_tag = channel.basic_consume(queue='task_queue', on_message_callback=callback2)
    print(consumer_tag)

    channel.basic_ack(delivery_tag=method.delivery_tag)

consumer_tag = channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.basic_qos(prefetch_count=1)
channel.start_consuming()