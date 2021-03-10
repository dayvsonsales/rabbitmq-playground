import pika

conn = pika.BlockingConnection()

ch = conn.channel()

for i in xrange(10000000):
    ch.basic_publish("", "perf", "abc")