import json
import os
from crawl import Pulls
from error import LambdaError


def main(event, context):
    organization = __get_param(event, "organization")
    user = __get_param(event, "user")
    fromDate = __get_param(event, "from")
    until = __get_param(event, "until")

    access_token = os.environ['GITHUB_API_KEY']

    if access_token is None or access_token == "undefined":
        raise LambdaError("[InternalServerError] Missing GITHUB_API_KEY")

    pulls = Pulls(
        access_token,
        organization,
        user,
        fromDate,
        until
    )

    csv_string = pulls.as_csv()

    response = {
        "statusCode": 200,
        "body": csv_string
    }

    return response

def __get_param(event, name):
   value = event["pathParameters"][name]
   if value is None:
       raise LambdaError("[BadRequest] Missing Path Parameter: {name}")
   return value

