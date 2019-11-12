import boto3
import datetime
import json
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_DB_TABLE'])


def process_record(event):
    for record in event['Records']:
        id = record['messageId']
        body = json.loads(record['body'])
        message = json.loads(body['Message'])
        date = str(datetime.datetime.strptime(
            message['pubDate'], '%a, %d %b %Y %H:%M:%S %z').date())
        print(id, date, message)
    return id, date, message


def check_if_item_exists(date):
	response = table.query(
	    KeyConditionExpression=Key('date').eq(date)
	)
	exists = bool(response['Items'])
	return exists


def get_script(date):
    response = table.get_item(
        Key={
            'date': date
        }
    )
    item = response['Item']
    return item['script']


def initialize_script(date, message):
    table.put_item(
        Item={
            'date': date,
            'script': [message]
        }
    )


def update_script(date, new_script):
    table.update_item(
        Key={
            'date': date
        },
        UpdateExpression=f"SET script = :new_script",
        ExpressionAttributeValues={
            ':new_script': new_script
        }
    )


def lambda_handler(event, context):
    print(json.dumps(event))
    id, date, message = process_record(event)
    if not check_if_item_exists(date):
        initialize_script(date, message)
    else:
        script = get_script(date)
        script.append(message)
        update_script(date, script)
