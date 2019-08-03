import boto3
import sys
import botocore
from datetime import datetime

# return list of the instance tags
def get_instance_tags(ec2, instance_id):
    instance = ec2.Instance(instance_id)
    tag_list = instance.tags
    return tag_list


# looking for - Key: backup | Value: yes
# get 'Name' tag value
def get_tag_info(tags):
    backup = False
    name_tag = ""
    for tag in tags:
        if tag["Key"] == "backup".lower() and tag["Value"] == "yes".lower():
            backup = True
        if tag["Key"] == "Name":
            name_tag = tag["Value"]
    if backup:
        return name_tag
    sys.exit("--Backup tag not set. Exiting...")
    
    
def make_backup(ec2, name_tag, instance_id):
    now = datetime.now()
    ami_name = name_tag + "-backup " + now.strftime("%Y-%m-%d %H-%M-%S %Z")
    instance = ec2.Instance(instance_id)
    print("The AMI Name: " + ami_name)
    print("-- Starting AMI creation for " + instance.id)
    try:
        image = instance.create_image(
            Description=name_tag + " Backup",
            Name=ami_name
        )
        print("-- {0} from {1} is currently {2}.".format(image.id, instance.id, image.state))
    except botocore.exceptions.ClientError as e:
        sys.exit(str(e))
        
    
def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    
    instance_id = event['detail']['instance-id']
    try:
        tags = get_instance_tags(ec2, instance_id)
    except botocore.exceptions.ClientError as e:
        sys.exit(str(e))
    name_tag = get_tag_info(tags)
    make_backup(ec2, name_tag, instance_id)

    
    