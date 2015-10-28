#! /usr/bin/env python3
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.queue_declare(queue="hello", auto_delete=False)


def callback(msg):
    print(" [x] Received %r" % (msg.body,))


channel.basic_consume(queue='hello', callback=callback, no_ack=True)

print(" [*] Waiting for messages. To exit press CTRL+C")
try:
    while True:
        channel.wait()
except KeyboardInterrupt:
    channel.close()
    connection.close()
