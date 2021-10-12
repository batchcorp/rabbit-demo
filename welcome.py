import pika, os, time, json
import boto3
import jinja2
from botocore.exceptions import ClientError
import message_pb2

def format_email(msg):
  print(msg)
  read_proto = message_pb2.Message()
  read_proto.ParseFromString(msg)
  name = read_proto.account.full_name
  recipient = read_proto.account.email
  file_loader = jinja2.FileSystemLoader('templates')
  env = jinja2.Environment(loader=file_loader)
  template = env.get_template('welcome.j2')
  output = template.render(name=name, email=recipient)
  payload = output
  return payload, recipient;

def email(body, msg, recipient):
   sender = "support@batch.sh"
   recipient = recipient
   configuration_set = "batch-log"
   aws_region = "us-west-2"
   subject = "Welcome to Batch"
   charset = "UTF-8"
   body_text = "test"
   client = boto3.client('ses',region_name=aws_region)
   try:
       #Provide the contents of the email.
       response = client.send_email(
           Destination={
               'ToAddresses': [
                   recipient,
               ],
           },
           Message={
               'Body': {
                   'Html': {
                       'Charset': charset,
                       'Data': msg,
                   },
                   'Text': {
                       'Charset': charset,
                       'Data': body_text,
                   },
               },
               'Subject': {
                   'Charset': charset,
                   'Data': subject,
               },
           },
           Source=sender,
           # If you are not using a configuration set, comment or delete the
           # following line
           ConfigurationSetName=configuration_set,
       )
   # Display an error if something goes wrong.	
   except ClientError as e:
       print(e.response['Error']['Message'])
   else:
       print("Email sent! Message ID:"),
       print(response['MessageId'])
   return;

# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('ISB_SHARED_URL', 'amqp://guest:guest@127.0.0.1:5672/%2f')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='welcomeemail') # Declare a queue
channel.queue_bind(queue='welcomeemail', exchange='events', routing_key='messages.billing.create_account')




# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  body_html, recipient = format_email(body)
  email(body, body_html, recipient)

# set up subscription on the queue
channel.basic_consume('welcomeemail',
  callback,
  auto_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()

