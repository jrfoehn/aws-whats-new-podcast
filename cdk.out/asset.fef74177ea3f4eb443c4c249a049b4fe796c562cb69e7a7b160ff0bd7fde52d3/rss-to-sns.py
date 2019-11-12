import boto3
import json
import os
from boto3.dynamodb.conditions import Key, Attr
from botocore.vendored import requests
from xml.etree import ElementTree

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_DB_TABLE'])

sns = boto3.client('sns')
topic = os.environ['SNS_TOPIC']

# Helper class to convert a DynamoDB item to JSON.


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get_rss_feed():
    response = requests.get(
        "https://aws.amazon.com/about-aws/whats-new/recent/feed/")
    tree = ElementTree.fromstring(response.content)
    items = tree.findall('channel/item')

    news_list = [{element.tag: element.text for element in item}
                 for item in items]

    return news_list


def check_if_exists(news):
    guid = news['guid']
    response = table.get_item(
        Key={
            'guid': guid
        }
    )

    if "Item" in response:
        return True
    else:
        return False


def put_item(news):
    table.put_item(
        Item=news
    )


def send_to_sns(news):
    category = news['category']
    needle = "general:products/"
    attribute_dict = {'NoAttributes': {
        'DataType': 'String', 'StringValue': 'NoAttributes'}}
    if category is not None:
        category_list = category.split(',')
        attributes = [x.replace(needle, '')
                      for x in category_list if needle in x]
        if len(attributes) > 0:
            attribute_dict = {x: {'DataType': 'String',
                                  'StringValue': x} for x in attributes}

    response = sns.publish(
        TopicArn=topic,
        Message=json.dumps(news),
        MessageAttributes=attribute_dict
    )


def lambda_handler(event, context):
    news_list = get_rss_feed()
    for news in news_list:
        is_sent = check_if_exists(news)
        if not is_sent:
            put_item(news)
            send_to_sns(news)
