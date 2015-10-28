#! /usr/bin/env python3
import amqp
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = amqp.Connection(host="localhost")
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            callback=self.on_response,
            no_ack=True
        )

    def on_response(self, message):
        if self.correlation_id == message.properties['correlation_id']:
            self.response = message.body

    def call(self, n):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        message = amqp.Message(
            body=str(n),
            reply_to=self.callback_queue,
            correlation_id=self.correlation_id
        )
        self.channel.basic_publish(
            message,
            exchange="",
            routing_key="rpc_queue"
        )
        while self.response is None:
            self.connection.drain_events()
        return int(self.response)


if __name__ == '__main__':
    fibonacci_rpc = FibonacciRpcClient()
    print(" [x] Requesting fib(30)")
    response = fibonacci_rpc.call(30)
    print(" [.] Got %r" % (response,))
