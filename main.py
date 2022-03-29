import boto3
import os


s3 = boto3.resource('s3')

BUCKET = s3.Bucket("codebucket234")
PREFIX: str = "consolidated"

def get_access_token():
    env_file = os.getenv("GITHUB_ENV")
    with open(env_file, 'r') as f:
        pass


def check_object_exists(prefix):
    objects = [*bucket.objects.filter(Prefix=prefix)]
    return bool(len(objects))



object_exists: bool = check_object_exists(PREFIX)

if object_exists:
    pass

    