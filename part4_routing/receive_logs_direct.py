#! /usr/bin/env python3
import sys
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.exchange_declare(exchange="direct_logs", type="direct")

result = channel.queue_declare(exclusive=True)
queue_name = result.queue

severities = sys.argv[1:]
if not severities:
    print("Usage: %s [info] [warning] [error]" % (sys.argv[0],),
          file=sys.stderr)
    sys.exit(1)

for severity in severities:
    channel.queue_bind(
        exchange="direct_logs",
        queue=queue_name,
        routing_key=severity
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
