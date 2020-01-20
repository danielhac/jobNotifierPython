from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import datetime
import pytz
from pytz import timezone
import credentials

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# AWS Lambda function
# Retrieve jobs from the DB that are found today and send results via E-mail
def my_function(event, context):
    # Helper class to convert a DynamoDB item to JSON.
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    # Get the service resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Jobs')

    # Convert server time to US Pacific Time in format: 'year-month-day' 
    date = datetime.datetime.utcnow()
    date = date.replace(tzinfo=pytz.UTC)
    date = date.astimezone(pytz.timezone("US/Pacific"))
    date = str(date.strftime("%Y-%m-%d"))
    
    print('Finding new jobs...')

    # Search parameters: get all links equal to today's date
    fe = Key('link').gte('a') & Key('date').eq(date)
    pe = "link, title, #dt, company"
    
    # Expression Attribute Names for Projection Expression only.
    ean = { "#dt": "date" }

    # Variable that will be used to append new jobs to
    if event != []:
        job_info = 'Websites that did not work: ' + str(event) + '\n\n'
    else:
        job_info = ''

    # Scan table in DB
    response = table.scan(
        FilterExpression=fe,
        ProjectionExpression=pe,
        ExpressionAttributeNames=ean
        )

    # Gather new jobs in DB
    for i in response['Items']:
        job_info += json.dumps(i, cls=DecimalEncoder) + '\n\n'


    ##### Email

    # Set up SMTP server
    s = smtplib.SMTP_SSL(host=credentials.host, port=credentials.port)
    s.login(credentials.user, credentials.passsword)

    # Create message
    msg = MIMEMultipart()
    msg['From'] = credentials.user
    msg['To'] = credentials.user
    if job_info == '':
        msg['Subject'] = "No New Jobs Today"
    else:
        msg['Subject'] = "Found New Jobs!"
    
    # Message body
    msg.attach(MIMEText(job_info, 'plain'))
    
    # Send E-mail
    s.send_message(msg)
    del msg
        
    # Terminate SMTP session and close the connection
    s.quit()


##### Comment out when running on AWS Lambda
# my_function('','')
