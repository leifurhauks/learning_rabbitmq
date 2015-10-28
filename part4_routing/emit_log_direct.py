#! /usr/bin/env python3
import sys
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.exchange_declare(exchange="direct_logs", type="direct")

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
body = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(
    amqp.Message(body=body),
    exchange="direct_logs",
    routing_key=severity
)
print(" [x] Sent %r:%r" % (severity, body))

channel.close()
connection.close()
