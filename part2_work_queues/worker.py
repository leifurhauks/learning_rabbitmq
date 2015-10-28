#! /usr/bin/env python3
import time
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.queue_declare(queue="task_queue", auto_delete=False, durable=True)


def callback(msg):
    print(" [x] Received %r" % (msg.body,))
    time.sleep(msg.body.count('.'))
    print(" [x] Done")
    channel.basic_ack(msg.delivery_tag)

channel.basic_qos(prefetch_count=1, prefetch_size=0, a_global=False)
channel.basic_consume(queue="task_queue", callback=callback, no_ack=False,
                      consumer_tag="foo")

print(" [*] Waiting for messages. To exit press CTRL+C")
try:
    while True:
        channel.wait()
except KeyboardInterrupt:
    channel.basic_cancel("foo")
    channel.close()
    connection.close()
