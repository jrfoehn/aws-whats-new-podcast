import boto3
import datetime
import json
import os
from boto3.dynamodb.conditions import Key, Attr

polly = boto3.client('polly')

bucket = os.environ['S3_BUCKET']


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_DB_TABLE'])

yesterday = (datetime.datetime.now() - datetime.timedelta(1))
yesterday_str = yesterday.strftime('%Y/%m/%d')
yesterday_str = "2019/11/08"
# today = datetime.datetime.now()
# date = today.strftime("%Y/%m/%d")
# date = "2019/10/18"


def get_script():
    response = table.get_item(
        Key={
            'date': yesterday_str
        }
    )
    item = response['Item']
    return item['script']


def generate_audio(raw_script):
    month = yesterday.strftime("%B")
    day = yesterday.strftime("%d")
    raw_script_len = len(raw_script)
    audio_script = f"<speak> <amazon:domain name='news'> There has been {raw_script_len} new announcements on {month} {day}. <break strength='x-strong'/> "

    for i in range(0, raw_script_len):
        audio_script = f"{audio_script} #{i+1}. {raw_script[i]['title']}. <break strength='strong'/>"

    audio_script = f"{audio_script} </amazon:domain> </speak>"

    return audio_script


def send_to_polly(audio_script):
    response = polly.start_speech_synthesis_task(
        Engine='neural',
        VoiceId='Joanna',
        OutputS3BucketName=bucket,
        OutputS3KeyPrefix="{}/".format(yesterday_str),
        OutputFormat='mp3',
        Text=audio_script,
        TextType='ssml')
    task_id = response['SynthesisTask']['TaskId']
    return task_id


def lambda_handler(event, context):
    raw_script = get_script()
    audio_script = generate_audio(raw_script)
    print(audio_script)
    task_id = send_to_polly(audio_script)
    print(task_id)
