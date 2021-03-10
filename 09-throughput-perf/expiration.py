import pika

# This files test the TTL expiration header in order to know how it behavior with same TTL and big TTL in the head of queue

conn = pika.BlockingConnection()
ch = conn.channel()

ch.exchange_declare(exchange='expira_dl',
                         exchange_type='direct')

result = ch.queue_declare(queue='expira_queue')
queue_name = result.method.queue
ch.queue_bind(exchange='expira_dl',
                   routing_key='expira_queue',
                   queue=queue_name)


ch.queue_declare(queue="expira", arguments={
    "x-dead-letter-exchange": 'expira_dl',
    "x-dead-letter-routing-key": "expira_queue"
})

ch.basic_publish(exchange='', routing_key='expira', body='teste1', properties=pika.BasicProperties(expiration="20000"))
ch.basic_publish(exchange='', routing_key='expira', body='teste2', properties=pika.BasicProperties(expiration="10000"))
ch.basic_publish(exchange='', routing_key='expira', body='teste3', properties=pika.BasicProperties(expiration="10000"))

print "Sent"
