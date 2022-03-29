import os


def get_access_token():
    access_token = os.environ.get("access_token")
    return access_token

print(f"access token is {get_access_token()}")

"""s3 = boto3.resource('s3')
BUCKET = s3.Bucket("codebucket234")
PREFIX: str = "consolidated"


def check_object_exists(prefix):
    objects = [*bucket.objects.filter(Prefix=prefix)]
    return bool(len(objects))



object_exists: bool = check_object_exists(PREFIX)

if object_exists:
    pass
    # use access token to call workflow

"""