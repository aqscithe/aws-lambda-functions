import boto3
import sys
import botocore
from datetime import datetime

def filter_instances(ec2, key, value):
    filters = [
            {
                'Name':'tag:' + key,
                'Values':[value, value.lower(), value.upper()]
            }
        ]
    if len(list(ec2.instances.filter(Filters=filters))):
        return ec2.instances.filter(Filters=filters)
    sys.exit("-- No instances with Backup tag and/or value not set to 'yes'.")


def start_backup(instances):
    was_running = False
    image = None
    for i in instances:
        if i.state['Name'] == 'terminated':
            continue
        elif i.state['Name'] == 'running':
            was_running = True
            try:
                print("-- Stopping {0} to make backup AMI...".format(i.id))
                i.stop()
            except botocore.exceptions.ClientError as e:
                print(str(e))
                continue
            i.wait_until_stopped()
        make_backup(i)
        if was_running:
            print("-- Starting {0}...".format(i.id))
            i.start()
        
        
def make_backup(i):
    name_tag = get_name_tag(i)
    now = datetime.now()
    ami_name = name_tag + "-backup " + now.strftime("%Y-%m-%d %H-%M-%S %Z")
    print("The AMI Name: " + ami_name)
    print("-- Starting {0} AMI creation...".format(i.id))
    try:
        image = i.create_image(
            Description=" Backup",
            Name=ami_name
        )
        print("-- {0} from {1} is currently {2}.".format(image.id, i.id, image.state))
    except botocore.exceptions.ClientError as e:
        print("{2} \n{0} is currently in the {1} state.".format(i.id, i.state['Name'], str(e)))
    
def get_name_tag(i):
    for tag in i.tags:
        if tag["Key"] == "Name":
            return tag["Value"]
            
def lambda_handler(event, context):
    print(event)
    key = 'Backup'
    value = 'Yes'
    ec2 = boto3.resource('ec2')
    instances = filter_instances(ec2, key, value)
    start_backup(instances)
