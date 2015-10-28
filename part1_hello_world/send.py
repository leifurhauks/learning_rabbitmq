#! /usr/bin/env python3
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.queue_declare(queue="hello", auto_delete=False)

msg = amqp.Message(body="Hello World!")
channel.basic_publish(msg, exchange="", routing_key="hello")
print(" [x] Sent 'Hello World!'")

connection.close()
