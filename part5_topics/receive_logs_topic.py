#! /usr/bin/env python3
import sys
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.exchange_declare(exchange="topic_logs", type="topic")

result = channel.queue_declare(exclusive=True)
queue_name = result.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    print("Usage: %s [binding_key]..." % (sys.argv[0],),
          file=sys.stderr)
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange="topic_logs",
        queue=queue_name,
        routing_key=binding_key
    )

def callback(message):
    print(" [x] %r:%r" % (message.delivery_info['routing_key'], message.body))

print("[*] Waiting for logs. To exit press CTRL+C")
channel.basic_consume(queue=queue_name, callback=callback, no_ack=True)

try:
    while True:
        channel.wait()
except KeyboardInterrupt:
    channel.close()
    connection.close()
