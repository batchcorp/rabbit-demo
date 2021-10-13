import pika, os, time, json
import jinja2




connection = pika.BlockingConnection(
    parameters = pika.URLParameters('amqp://guest:guest@127.0.0.1:5672/%2F'))
channel = connection.channel()

channel.queue_declare(queue='welcome')
channel.queue_bind(queue='welcome', exchange='event', routing_key='messages.billing.create_account')

with open('json-data.json') as json_file:
    data = json.load(json_file)

for message in data:
    channel.basic_publish(exchange='event', routing_key='messages.billing.create_account', body=json.dumps(message))
    print("Json sent ")

connection.close()