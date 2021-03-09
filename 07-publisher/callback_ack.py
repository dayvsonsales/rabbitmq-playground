import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

def on_delivery_confirmation(frame):
    print(frame)

channel.confirm_delivery()

try:
    channel.basic_publish(exchange='', routing_key='aaa', body="Dayvson", mandatory=True, properties=pika.BasicProperties(content_type='text/plain',
                                                          delivery_mode=1))

    print("Message sent and confirmed")
except Exception as err:
    print(err)
    print("Message not sent to any queue")
    pass