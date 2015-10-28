#! /usr/bin/env python3
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.exchange_declare(exchange="logs", type="fanout")

result = channel.queue_declare(exclusive=True)
queue_name = result.queue

channel.queue_bind(exchange="logs", queue=queue_name)


def callback(message):
    print(" [x] %r" % (message.body,))


print(" [*] Waiting for logs. To exit press CTRL+C")
channel.basic_consume(queue=queue_name, callback=callback, no_ack=True)

try:
    while True:
        channel.wait()
except KeyboardInterrupt:
    channel.close()
    connection.close()
