import pika

class TaskQueue:

    def __init__(self, url_parameters):
        parameters  = pika.URLParameters(url_parameters)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.queue_name = 'task_queue'

    def get_queue_length(self):
        queue = self.connection.channel().queue_declare(queue=self.queue_name, durable=True, passive=True)
        return queue.method.message_count

    def perform_task(self, task):
        self.channel.basic_qos(prefetch_count=1)
        for method_frame, properties, body in self.channel.consume(self.queue_name):
            task(body)
            self.channel.basic_ack(method_frame.delivery_tag)
            break

    def publish_message(self, message):
        self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))

    def close(self):
        self.connection.close()