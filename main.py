import os
import boto3
from typing import final
import json
import requests

############## CONSTANTS #################

s3 = boto3.resource('s3')
BUCKET = s3.Bucket("codebucket234")
PREFIX: str = "consolidated"
CONFIG_FILE: final = "./config.json"
ACCESS_TOKEN: final = "access_token"
OWNER: final = "owner"
REPO: final = "repository"
API: final = "api"
TRIGGER_REQUEST: final = "trigger"
EVENT_TYPE: final = "product1_inference"
PROCESSED_FILES_FOLDER: str = 'processed_files/'


############## HELPERS #################

def check_object_exists(prefix):
    all_objects = [*BUCKET.objects.filter(Prefix=prefix)]

    previously_processed_files = {pf.key.split('/')[-1] for pf in BUCKET.objects.filter(Prefix='processed_files/')}

    files_to_be_processed = []

    for ob in all_objects:
        if ob.key not in previously_processed_files:
            files_to_be_processed.append(ob.key)

    for ob in all_objects:
        current_object_key = ob.key

        copy_source = {
            'Bucket': 'codebucket234',
            'Key': current_object_key
        }

        s3.meta.client.copy(copy_source, "codebucket234", f"{PROCESSED_FILES_FOLDER}{current_object_key}")

    return bool(len(files_to_be_processed))


def get_access_token():
    access_token = os.environ.get(ACCESS_TOKEN)
    return access_token


def get_config_file_details(config_file_path: str):
    with open(config_file_path, "r") as f:
        config = json.load(f)
    return config


object_exists: bool = check_object_exists(PREFIX)

if object_exists:
    access_token: str = get_access_token()
    config = get_config_file_details(CONFIG_FILE)
    owner: str = config[OWNER]
    repo: str = config[REPO]
    trigger_req_api: str = config[API][TRIGGER_REQUEST]

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    trigger_request: str = trigger_req_api.format(owner=owner, repo=repo)
    event_data = {"event_type": EVENT_TYPE}

    response = requests.post(
        url=trigger_request,
        headers=headers,
        data=json.dumps(event_data)
    )

    print(response.ok, response.content)
