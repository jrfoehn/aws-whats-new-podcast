import boto3
import os
import sys
import time
import datetime
from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr
import feedparser

sqs = boto3.client('sqs')
sqs_url = os.environ['SQS_URL']

rss_url = os.environ['RSS_URL']

today = datetime.datetime.now().strftime("%Y/%m/%d")
today = "2019/10/18"


def get_rss(url):
	return feedparser.parse(url)


def send_message(id, date, title):
    response = sqs.send_message(
        QueueUrl=sqs_url,
        DelaySeconds=10,
        MessageAttributes={
            'id': {
                'DataType': 'String',
                'StringValue': id
            },
            'date': {
            	'DataType': 'String',
            	'StringValue': date
            }
        },
        MessageBody=(
            title
        )
    )
    return response['MessageId']


def lambda_handler(event, context):
	feed = get_rss(rss_url)

	for item in feed['entries']:
		id = item['id']
		blog_url = item['link']
		date = "{}/{}/{}".format(item['published_parsed'][0],
		                         item['published_parsed'][1], item['published_parsed'][2])
		title = item['title'].encode('utf-8')
		if date == today:
			sqs_message_id = send_message(id, date, title)
			print(sqs_message_id)
