# RabbitMQ tutorial code with py-amqp
## Comments, suggestions, corrections welcome

This is python code I wrote while learning a bit about [RabbitMQ](https://rabbitmq.com/).

The directories `partN_...` contain code I wrote while following the rabbitmq
python [tutorial](https://www.rabbitmq.com/tutorials/tutorial-one-python.html).
That tutorial is written for the `pika` library, but I adapted it for the
[py-amqp](http://amqp.readthedocs.org) library instead.

The `rabbits_and_warrens` directory contains code I wrote while following
[Rabbits and warrens](http://blogs.digitar.com/jjww/2009/01/rabbits-and-warrens/),
Jason Williams' introduction to RabbitMQ.

If you spot any issues or have suggestions I'd love to hear them.

One thing I'm not clear on is the difference between `channel.wait()` and
`connection.drain_events()`. If anyone can answer that I'd be much obliged :-)

Also, is `connection.drain_events` in pyamqp really equivalent to pika's
`connection.process_data_events`, or did I just erroneously make that up?
