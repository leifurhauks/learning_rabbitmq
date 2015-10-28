#! /usr/bin/env python3
import sys
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.exchange_declare(exchange="topic_logs", type="topic")

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
body = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(
    amqp.Message(body=body),
    exchange="topic_logs",
    routing_key=routing_key
)
print(" [x] Sent %r:%r" % (routing_key, body))

channel.close()
connection.close()
