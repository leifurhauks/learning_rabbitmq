#! /usr/bin/env python3
import sys
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.exchange_declare(exchange="logs", type="fanout")

body = ' '.join(sys.argv[1:]) or "info: Hello World!"
message = amqp.Message(body=body)
message.properties['delivery_mode'] = 2

channel.basic_publish(message, exchange="logs", routing_key="")

print(" [x] Sent %r" % (message.body,))
connection.close()
