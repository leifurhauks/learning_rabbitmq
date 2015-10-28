#! /usr/bin/env python3
import sys
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.queue_declare(queue="task_queue", auto_delete=False, durable=True)

body = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(
    amqp.Message(body=body, delivery_mode=2),
    exchange='',
    routing_key='task_queue'
)
print(" [x] Sent %r" % (body,))

channel.close()
connection.close()
