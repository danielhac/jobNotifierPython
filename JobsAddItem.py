from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import datetime
import pytz
from pytz import timezone
from boto3.dynamodb.conditions import Key, Attr


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Get the service resource
dynamodb = boto3.resource('dynamodb')

# Instantiate a table resource object
table = dynamodb.Table('Jobs')

# Convert server time to US Pacific Time in format: 'year-month-day'
dt = datetime.datetime.utcnow()
dt = dt.replace(tzinfo=pytz.UTC)
dt = dt.astimezone(pytz.timezone("US/Pacific"))
dt = str(dt.strftime("%Y-%m-%d"))

# Add job info to DB
def addjob(title, company, link):
    try:
        response = table.put_item(
        Item={
                # 'date': '2020-01-13',
                'date': dt,
                'title': title,
                'company': company,
                'link': link
            },
            # If URL exists, do not add to DB
            ConditionExpression = 'attribute_not_exists(link)'
        )
        print("PutItem succeeded:")
        # print(json.dumps(response, indent=4, cls=DecimalEncoder))
    except:
        print("Already exists in DB")
