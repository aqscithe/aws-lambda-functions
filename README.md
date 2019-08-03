# aws-lambda-functions

## create-image
Creates a AMI backups of instances based on instance tagging. Triggered by CloudWatch events - instance changing to stopped state.

Sample Event:
```
{
  "version": "0",
  "id": "6d824bba-1df7-61da-e73d-5236c8d0c0ef",
  "detail-type": "EC2 Instance State-change Notification",
  "source": "aws.ec2",
  "account": "110010011001",
  "time": "2016-01-03T11:39:38Z",
  "region": "us-east-1",
  "resources": [
    "arn:aws:ec2:us-east-1:110010011001:instance/i-03067fbc0d6d8abed"
  ],
  "detail": {
    "instance-id": "i-03067fbc0d6d8abed",
    "state": "stopped"
  }
}
```
## create-image-schedule
Creates a AMI backups of instances based on instance tagging. Triggered by CloudWatch events schedule. This function doesn't take any parameters from the event, so it could be triggered by whatever you want.
