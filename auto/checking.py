import subprocess

import boto3

# Create a session using your AWS credentials


def refreshSecurityToken(self):
    p = subprocess.Popen(['okta-awscli', '--profile', 'core', '--okta-profile', 'core'])
    print(p.communicate())
url = "https://rtb-bid-price-prod-east.vpce-0b38fbb31ac1579ed-ilolr9fy.s3.us-east-1.vpce.amazonaws.com/"
s3_client = boto3.client("s3", region_name="us-east-1")

response =  s3_client.list_objects(Bucket=url)

print(response)
# Create an S3 client using the session
# s3_client = session.client('s3')

# Specify the bucket name
# bucket_name = 'your-bucket-name'

# List objects in the bucket
# response = s3_client.list_objects(Bucket=bucket_name)

# Print object keys
# if 'Contents' in response:
#     for obj in response['Contents']:
#         print(obj['Key'])
# else:
#     print("Bucket is empty or does not exist")
