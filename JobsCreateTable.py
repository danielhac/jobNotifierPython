from __future__ import print_function # Python 2/3 compatibility
import boto3

# Get the service resource
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

# Create table and define required attribute(s)
table = dynamodb.create_table(
    TableName='Jobs',
    
    # All items with the same partition key value are stored together, in sorted order by sort key value
    KeySchema=[
        {
            'AttributeName': 'link',
            'KeyType': 'HASH'  #Partition key
        },
        # {
        #     'AttributeName': 'date',
        #     'KeyType': 'RANGE'  #Sort key
        # }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'link',
            'AttributeType': 'S'
        },
        # {
        #     'AttributeName': 'date',
        #     'AttributeType': 'S'
        # },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)
