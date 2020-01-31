from flask import Flask, jsonify, request, make_response
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import datetime
import pytz
from pytz import timezone
import base64

application = Flask(__name__)


# Create response
def resOutput(msg, mime, code):
    res = make_response(msg)
    res.mimetype = mime
    res.status_code = code
    return res


# Convert server time to US Pacific Time in format: 'year-month-day' 
def date_pacific():
    date = datetime.datetime.utcnow()
    date = date.replace(tzinfo=pytz.UTC)
    date = date.astimezone(pytz.timezone("US/Pacific"))
    date = str(date.strftime("%Y-%m-%d"))
    return date


@application.route('/')
def index():
    return ('Try path /jobs')


# Get all items or create an item
@application.route('/jobs', methods=['GET', 'POST'])
def jobs():
    # Get the service resource
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('Jobs')
    
    # Get all items
    if request.method == 'GET':    
        # Search parameters: get all links - NOTE: can add filters later
        fe = Key('link').gte('a')
        pe = "link, title, #dt, company"
        
        # Expression Attribute Names for Projection Expression only.
        ean = { "#dt": "date" }

        # Scan table in DB
        response = table.scan(
            FilterExpression=fe,
            ProjectionExpression=pe,
            ExpressionAttributeNames=ean
            )
        return resOutput(json.dumps(response['Items']), 'application/json', 201)

    # Create an item
    elif request.method == 'POST':        
        content = request.get_json()

        # Ensure all attributes exist
        if "title" not in content or "company" not in content or "link" not in content:
            return resOutput('{"Error": "The request object is missing at least one of the required attributes"}', "application/json", 400)
        
        # Add job info to DB
        try:
            response = table.put_item(
                Item={
                        'date': date_pacific(),
                        'title': content['title'],
                        'company': content['company'],
                        'link': content['link']
                    },
                    # If URL exists, do not add to DB
                    ConditionExpression = 'attribute_not_exists(link)'
            )
            print("PutItem succeeded:")
            print(response)
        except:
            print("Already exists in DB")
            return resOutput('{"Error": "Already exists in DB"}', "application/json", 400)
        return resOutput(json.dumps(content), 'application/json', 201)
    
    
# Route for 1 item
# Since the 'id' is an actual URL, it will need to be converted to alpha-numeric such as base64 
@application.route('/jobs/<id>', methods=['GET', 'PUT', 'DELETE'])
def one_job(id):
    # Decode URL from base64 to 'b' string
    decoded_id = base64.b64decode(id)
    decoded_id = str(decoded_id).split('b')[1]
    print(decoded_id[1:-1])

    # Get the service resource
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('Jobs')

    # Get 1 item
    if request.method == 'GET':
        try:
            response = table.get_item(
                Key={
                    'link': decoded_id[1:-1]
                }
            )
            print(response)
            return resOutput(json.dumps(response['Item']), 'application/json', 201)
        except:
            print("Not found in DB")
            return resOutput('{"Error": "Not found in DB"}', "application/json", 400)
    
    # Update item attributes
    elif request.method == 'PUT':
        # Get the item first as a workaround for updating attributes
        try:
            response_item = table.get_item(
                Key={
                    'link': decoded_id[1:-1]
                }
            )
            response_item = response_item['Item']
        except:
            print("Not found in DB")
            return resOutput('{"Error": "Not found in DB"}', "application/json", 400)

        content = request.get_json()

        # Obtain new content from attributes
        if "title" in content or "company" in content:
            if "title" in content:
                response_item['title'] = content['title']
            if "company" in content:
                response_item['company'] = content['company']
        else:
            return resOutput('{"Error": "The request object is missing at least one of the required attributes"}', "application/json", 400)

        # Update job info
        try:
            response = table.update_item(
                Key={
                    'link': decoded_id[1:-1]
                },
                UpdateExpression="SET title = :val1, company = :val2",
                ExpressionAttributeValues={
                    ':val1': response_item['title'],
                    ':val2': response_item['company']
                },
                ReturnValues='ALL_NEW'
            )
            print("PutItem succeeded:")
        except:
            return resOutput('{"Error": "Not found in DB"}', "application/json", 400)
        return resOutput(json.dumps(response), 'application/json', 201)
    
    # Delete 1 item
    elif request.method == 'DELETE':
        try:
            table.delete_item(
                Key={
                    'link': decoded_id[1:-1]
                }
            )
        except:
            return resOutput('{"Error": "Not found in DB"}', "application/json", 400)
        return ('',204)


if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)
