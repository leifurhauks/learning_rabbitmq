#! /usr/bin/env python3
import amqp

connection = amqp.Connection(host="localhost")
channel = connection.channel()

channel.queue_declare(queue="rpc_queue")


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def on_request(message):
    n = int(message.body)

    print( " [.] fib(%s)" % (n,))
    result = fib(n)
    response = amqp.Message(body=str(result))
    response.properties['correlation_id'] = message.properties['correlation_id']

    message.channel.basic_publish(
        response,
        exchange="",
        routing_key=message.properties['reply_to']
    )
    message.channel.basic_ack(delivery_tag=message.delivery_tag)


channel.basic_qos(prefetch_count=1, prefetch_size=0, a_global=False)
channel.basic_consume(queue="rpc_queue", callback=on_request,
                      consumer_tag="rpc_server")

print(" [x] Awaiting RPC requests")
try:
    while True:
        connection.drain_events()
except KeyboardInterrupt:
    channel.basic_cancel("rpc_server")
    channel.close()
    connection.close()
