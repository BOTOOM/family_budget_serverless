import json
import pandas as pd



# import requests


def lambda_handler(event, context):



    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello worlddd",
        }),
    }
