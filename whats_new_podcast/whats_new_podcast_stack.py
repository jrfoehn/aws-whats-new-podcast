from aws_cdk import (
    core,
    cx_api  as _cx,
    aws_dynamodb    as _ddb,
    aws_events      as _events,
    aws_events_targets as _targets,
    aws_iam         as _iam,
    aws_lambda      as _lambda,
    aws_lambda_event_sources as _lambda_events,
    aws_s3          as _s3,
    aws_sns         as _sns,
    aws_sns_subscriptions as _sns_subs,
    aws_sqs         as _sqs,
)
import random


class WhatsNewPodcastStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ddb_whats_new_podcast = _ddb.Table(
            self, 'whats-new-podcast-table',
            partition_key   = {
                'name': 'guid',
                'type': _ddb.AttributeType.STRING
            },
            table_name = 'whats-new-podcast',
        )

        ddb_script = _ddb.Table(
            self, 'whats-new-podcast-script',
            partition_key = {
                'name': 'date',
                'type': _ddb.AttributeType.STRING
            },
            table_name = 'whats-new-podcast-script'
        )

        sqs_whats_new_podcast = _sqs.Queue(
            self, 'whats-new-podcast-queue',
            queue_name = 'whats-new-podcast-queue',
        )

        sns_whats_new_podcast = _sns.Topic(
            self, 'whats-new-podcast-topic',
            display_name = 'AWS News',
            topic_name   = 'whats-new-podcast-topic',
        )
        sns_whats_new_podcast.add_subscription(_sns_subs.SqsSubscription(sqs_whats_new_podcast))

        s3_podcast_bucket = _s3.Bucket(
            self, "whats-new-podcast-bucket",
            bucket_name = f"whats-new-podcast-bucket-{random.randrange(1000000000)}"
        )


        statement_sns_publish = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            actions=[
                'sns:Publish'
            ],
            resources=[
                sns_whats_new_podcast.topic_arn
            ]
        )
        statement_dynamodb = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            actions=[
                'dynamodb:PutItem',
                'dynamodb:GetItem'
            ],
            resources=[
                ddb_whats_new_podcast.table_arn
            ]
        )

        lambda_rss_to_sns = _lambda.Function(
            self, 'whats-new-podcast-rss-to-sns',
            runtime     = _lambda.Runtime.PYTHON_3_7,
            code        = _lambda.Code.asset('lambda/rss-to-sns'),
            handler     = 'rss-to-sns.lambda_handler',
            environment = {
                'DYNAMO_DB_TABLE': ddb_whats_new_podcast.table_name,
                'SNS_TOPIC': sns_whats_new_podcast.topic_arn
            },
            function_name = 'whats-new-podcast-rss-to-sns',
            timeout     = core.Duration.seconds(30),
        )
        lambda_rss_to_sns.add_to_role_policy(statement_dynamodb)
        lambda_rss_to_sns.add_to_role_policy(statement_sns_publish)

        rule_rss = _events.Rule(
            self, 'whats-new-podcast-rss-rule',
            schedule=_events.Schedule.cron(
                minute='0/15',
                hour='1-23/2',
                month='*',
                week_day='*',
                year='*'
            ),
            rule_name = 'whats-new-podcast-rss-rule'
        )
        rule_rss.add_target(_targets.LambdaFunction(lambda_rss_to_sns))

        lambda_generate_script = _lambda.Function(
            self, 'whats-new-podcast-generate-script',
            runtime = _lambda.Runtime.PYTHON_3_7,
            code    = _lambda.Code.asset('lambda/generate-script'),
            handler = 'generate-script.lambda_handler',
            environment     = {
                'DYNAMO_DB_TABLE': ddb_script.table_name
            },
            function_name   = 'whats-new-podcast-generate-script',
            timeout = core.Duration.seconds(30),
        )
        statement_lambda_generate_script_ddb = _iam.PolicyStatement(
            effect = _iam.Effect.ALLOW,
            actions= [
                'dynamodb:PutItem',
                'dynamodb:GetItem',
                'dynamodb:Query',
                'dynamodb:UpdateItem',
            ],
            resources = [
                ddb_script.table_arn
            ]
        )
        lambda_generate_script.add_to_role_policy(statement_lambda_generate_script_ddb)
        lambda_generate_script_source_queue = _lambda_events.SqsEventSource(
            queue = sqs_whats_new_podcast,
            batch_size = 1
        )
        lambda_generate_script.add_event_source(lambda_generate_script_source_queue)


        lambda_generate_voice = _lambda.Function(
            self, 'whats-new-podcast-generate-voice',
            runtime = _lambda.Runtime.PYTHON_3_7,
            code    = _lambda.Code.asset('lambda/generate-voice'),
            handler = 'generate-voice.lambda_handler',
            environment = {
                'DYNAMO_DB_TABLE': ddb_script.table_name,
                'S3_BUCKET': s3_podcast_bucket.bucket_name
            },
            function_name = 'whats-new-podcast-generate-voice',
            timeout = core.Duration.seconds(30),
        )
        statement_lambda_generate_voice_ddb = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            actions=[
                'dynamodb:GetItem',
                'dynamodb:Query',
            ],
            resources=[
                ddb_script.table_arn
            ]
        )
        statement_lambda_generate_voice_polly = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            actions=[
                'polly:SynthesizeSpeech',
                'polly:StartSpeechSynthesisTask'
            ],
            resources=[
                '*'
            ]
        )
        statement_lambda_generate_voice_s3 = _iam.PolicyStatement(
            effect  = _iam.Effect.ALLOW,
            actions = [
                's3:PutObject'
            ],
            resources = [
                f"{s3_podcast_bucket.bucket_arn}/*"
            ]
        )
        lambda_generate_voice.add_to_role_policy(statement_lambda_generate_voice_ddb)
        lambda_generate_voice.add_to_role_policy(statement_lambda_generate_voice_polly)
        lambda_generate_voice.add_to_role_policy(statement_lambda_generate_voice_s3)

        rule_voice = _events.Rule(
            self, 'whats-new-podcast-generate-voice-rule',
            schedule=_events.Schedule.cron(
                minute='30',
                hour='0',
                month='*',
                week_day='*',
                year='*'
            ),
            rule_name='whats-new-podcast-generate-voice-rule'
        )
        rule_voice.add_target(_targets.LambdaFunction(lambda_generate_voice))

