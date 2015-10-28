import sys
import amqp

conn = amqp.Connection(
    host="localhost:5672",
    userid="guest",
    password="guest",
    virtual_host="/"
)
chan = conn.channel()


chan.queue_declare(
    queue="po_box",
    durable=True,
    exclusive=False,
    auto_delete=False
)
chan.exchange_declare(
    exchange="sorting_room",
    type="direct",
    durable=True,
    auto_delete=False
)

if len(sys.argv) > 1:
    text = sys.argv[1]
else:
    text = "Test message!"
msg = amqp.Message(text)
msg.properties["delivery_mode"] = 2
chan.basic_publish(msg, exchange="sorting_room", routing_key="jason")
