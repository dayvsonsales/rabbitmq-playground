import pika


conn = pika.BlockingConnection()
ch = conn.channel()

def callback(ch, method, properties, body):
    print " [x] %r" % (properties,)
    ch.basic_reject(delivery_tag=method.delivery_tag)

ch.basic_consume(queue='expira_queue', on_message_callback=callback)
ch.start_consuming()