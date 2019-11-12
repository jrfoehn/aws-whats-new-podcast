import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_apigateway
import aws_cdk.aws_dynamodb
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kinesis
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_s3_notifications
import aws_cdk.aws_sns
import aws_cdk.aws_sns_subscriptions
import aws_cdk.aws_sqs
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-lambda-event-sources", "1.15.0", __name__, "aws-lambda-event-sources@1.15.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class ApiEventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.ApiEventSource"):
    def __init__(self, method: str, path: str, *, api_key_required: typing.Optional[bool]=None, authorization_type: typing.Optional[aws_cdk.aws_apigateway.AuthorizationType]=None, authorizer: typing.Optional[aws_cdk.aws_apigateway.IAuthorizer]=None, method_responses: typing.Optional[typing.List[aws_cdk.aws_apigateway.MethodResponse]]=None, operation_name: typing.Optional[str]=None, request_models: typing.Optional[typing.Mapping[str,aws_cdk.aws_apigateway.IModel]]=None, request_parameters: typing.Optional[typing.Mapping[str,bool]]=None, request_validator: typing.Optional[aws_cdk.aws_apigateway.IRequestValidator]=None) -> None:
        """
        :param method: -
        :param path: -
        :param options: -
        :param api_key_required: Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_type: Method authorization. Default: None open access
        :param authorizer: If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource.
        :param method_responses: The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: The resources that are used for the response's content type. Specify request models as key-value pairs (string-to-string mapping), with a content type as the key and a Model resource name as the value
        :param request_parameters: The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: The ID of the associated request validator.
        """
        options = aws_cdk.aws_apigateway.MethodOptions(api_key_required=api_key_required, authorization_type=authorization_type, authorizer=authorizer, method_responses=method_responses, operation_name=operation_name, request_models=request_models, request_parameters=request_parameters, request_validator=request_validator)

        jsii.create(ApiEventSource, self, [method, path, options])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.IFunction) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        """
        return jsii.invoke(self, "bind", [target])


@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class S3EventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.S3EventSource"):
    """Use S3 bucket notifications as an event source for AWS Lambda."""
    def __init__(self, bucket: aws_cdk.aws_s3.Bucket, *, events: typing.List[aws_cdk.aws_s3.EventType], filters: typing.Optional[typing.List[aws_cdk.aws_s3.NotificationKeyFilter]]=None) -> None:
        """
        :param bucket: -
        :param props: -
        :param events: The s3 event types that will trigger the notification.
        :param filters: S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.
        """
        props = S3EventSourceProps(events=events, filters=filters)

        jsii.create(S3EventSource, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.IFunction) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        """
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.Bucket:
        return jsii.get(self, "bucket")


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-event-sources.S3EventSourceProps", jsii_struct_bases=[], name_mapping={'events': 'events', 'filters': 'filters'})
class S3EventSourceProps():
    def __init__(self, *, events: typing.List[aws_cdk.aws_s3.EventType], filters: typing.Optional[typing.List[aws_cdk.aws_s3.NotificationKeyFilter]]=None):
        """
        :param events: The s3 event types that will trigger the notification.
        :param filters: S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.
        """
        self._values = {
            'events': events,
        }
        if filters is not None: self._values["filters"] = filters

    @property
    def events(self) -> typing.List[aws_cdk.aws_s3.EventType]:
        """The s3 event types that will trigger the notification."""
        return self._values.get('events')

    @property
    def filters(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.NotificationKeyFilter]]:
        """S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules."""
        return self._values.get('filters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3EventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class SnsEventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.SnsEventSource"):
    """Use an Amazon SNS topic as an event source for AWS Lambda."""
    def __init__(self, topic: aws_cdk.aws_sns.ITopic) -> None:
        """
        :param topic: -
        """
        jsii.create(SnsEventSource, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.IFunction) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        """
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="topic")
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        return jsii.get(self, "topic")


@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class SqsEventSource(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.SqsEventSource"):
    """Use an Amazon SQS queue as an event source for AWS Lambda."""
    def __init__(self, queue: aws_cdk.aws_sqs.IQueue, *, batch_size: typing.Optional[jsii.Number]=None) -> None:
        """
        :param queue: -
        :param props: -
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. Default: 10
        """
        props = SqsEventSourceProps(batch_size=batch_size)

        jsii.create(SqsEventSource, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.IFunction) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        """
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="queue")
    def queue(self) -> aws_cdk.aws_sqs.IQueue:
        return jsii.get(self, "queue")


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-event-sources.SqsEventSourceProps", jsii_struct_bases=[], name_mapping={'batch_size': 'batchSize'})
class SqsEventSourceProps():
    def __init__(self, *, batch_size: typing.Optional[jsii.Number]=None):
        """
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. Default: 10
        """
        self._values = {
        }
        if batch_size is not None: self._values["batch_size"] = batch_size

    @property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range: Minimum value of 1. Maximum value of 10.

        default
        :default: 10
        """
        return self._values.get('batch_size')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SqsEventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.aws_lambda.IEventSource)
class StreamEventSource(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-lambda-event-sources.StreamEventSource"):
    """Use an stream as an event source for AWS Lambda."""
    @staticmethod
    def __jsii_proxy_class__():
        return _StreamEventSourceProxy

    def __init__(self, *, starting_position: aws_cdk.aws_lambda.StartingPosition, batch_size: typing.Optional[jsii.Number]=None, max_batching_window: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param props: -
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5). Default: Duration.seconds(0)
        """
        props = StreamEventSourceProps(starting_position=starting_position, batch_size=batch_size, max_batching_window=max_batching_window)

        jsii.create(StreamEventSource, self, [props])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, _target: aws_cdk.aws_lambda.IFunction) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -
        """
        ...

    @jsii.member(jsii_name="enrichMappingOptions")
    def _enrich_mapping_options(self, *, event_source_arn: str, batch_size: typing.Optional[jsii.Number]=None, enabled: typing.Optional[bool]=None, max_batching_window: typing.Optional[aws_cdk.core.Duration]=None, starting_position: typing.Optional[aws_cdk.aws_lambda.StartingPosition]=None) -> aws_cdk.aws_lambda.EventSourceMappingOptions:
        """
        :param options: -
        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis and Amazon DynamoDB is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param enabled: Set to false to disable the event source upon creation. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5). Default: Duration.seconds(0)
        :param starting_position: The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.
        """
        options = aws_cdk.aws_lambda.EventSourceMappingOptions(event_source_arn=event_source_arn, batch_size=batch_size, enabled=enabled, max_batching_window=max_batching_window, starting_position=starting_position)

        return jsii.invoke(self, "enrichMappingOptions", [options])

    @property
    @jsii.member(jsii_name="props")
    def _props(self) -> "StreamEventSourceProps":
        return jsii.get(self, "props")


class _StreamEventSourceProxy(StreamEventSource):
    @jsii.member(jsii_name="bind")
    def bind(self, _target: aws_cdk.aws_lambda.IFunction) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -
        """
        return jsii.invoke(self, "bind", [_target])


class DynamoEventSource(StreamEventSource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.DynamoEventSource"):
    """Use an Amazon DynamoDB stream as an event source for AWS Lambda."""
    def __init__(self, table: aws_cdk.aws_dynamodb.Table, *, starting_position: aws_cdk.aws_lambda.StartingPosition, batch_size: typing.Optional[jsii.Number]=None, max_batching_window: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param table: -
        :param props: -
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5). Default: Duration.seconds(0)
        """
        props = DynamoEventSourceProps(starting_position=starting_position, batch_size=batch_size, max_batching_window=max_batching_window)

        jsii.create(DynamoEventSource, self, [table, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.IFunction) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        """
        return jsii.invoke(self, "bind", [target])


class KinesisEventSource(StreamEventSource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-lambda-event-sources.KinesisEventSource"):
    """Use an Amazon Kinesis stream as an event source for AWS Lambda."""
    def __init__(self, stream: aws_cdk.aws_kinesis.IStream, *, starting_position: aws_cdk.aws_lambda.StartingPosition, batch_size: typing.Optional[jsii.Number]=None, max_batching_window: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param stream: -
        :param props: -
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5). Default: Duration.seconds(0)
        """
        props = KinesisEventSourceProps(starting_position=starting_position, batch_size=batch_size, max_batching_window=max_batching_window)

        jsii.create(KinesisEventSource, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: aws_cdk.aws_lambda.IFunction) -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -
        """
        return jsii.invoke(self, "bind", [target])

    @property
    @jsii.member(jsii_name="stream")
    def stream(self) -> aws_cdk.aws_kinesis.IStream:
        return jsii.get(self, "stream")


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-event-sources.StreamEventSourceProps", jsii_struct_bases=[], name_mapping={'starting_position': 'startingPosition', 'batch_size': 'batchSize', 'max_batching_window': 'maxBatchingWindow'})
class StreamEventSourceProps():
    def __init__(self, *, starting_position: aws_cdk.aws_lambda.StartingPosition, batch_size: typing.Optional[jsii.Number]=None, max_batching_window: typing.Optional[aws_cdk.core.Duration]=None):
        """The set of properties for event sources that follow the streaming model, such as, Dynamo and Kinesis.

        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5). Default: Duration.seconds(0)
        """
        self._values = {
            'starting_position': starting_position,
        }
        if batch_size is not None: self._values["batch_size"] = batch_size
        if max_batching_window is not None: self._values["max_batching_window"] = max_batching_window

    @property
    def starting_position(self) -> aws_cdk.aws_lambda.StartingPosition:
        """Where to begin consuming the stream."""
        return self._values.get('starting_position')

    @property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        default
        :default: 100
        """
        return self._values.get('batch_size')

    @property
    def max_batching_window(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5).

        default
        :default: Duration.seconds(0)
        """
        return self._values.get('max_batching_window')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StreamEventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-event-sources.DynamoEventSourceProps", jsii_struct_bases=[StreamEventSourceProps], name_mapping={'starting_position': 'startingPosition', 'batch_size': 'batchSize', 'max_batching_window': 'maxBatchingWindow'})
class DynamoEventSourceProps(StreamEventSourceProps):
    def __init__(self, *, starting_position: aws_cdk.aws_lambda.StartingPosition, batch_size: typing.Optional[jsii.Number]=None, max_batching_window: typing.Optional[aws_cdk.core.Duration]=None):
        """
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5). Default: Duration.seconds(0)
        """
        self._values = {
            'starting_position': starting_position,
        }
        if batch_size is not None: self._values["batch_size"] = batch_size
        if max_batching_window is not None: self._values["max_batching_window"] = max_batching_window

    @property
    def starting_position(self) -> aws_cdk.aws_lambda.StartingPosition:
        """Where to begin consuming the stream."""
        return self._values.get('starting_position')

    @property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        default
        :default: 100
        """
        return self._values.get('batch_size')

    @property
    def max_batching_window(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5).

        default
        :default: Duration.seconds(0)
        """
        return self._values.get('max_batching_window')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DynamoEventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-lambda-event-sources.KinesisEventSourceProps", jsii_struct_bases=[StreamEventSourceProps], name_mapping={'starting_position': 'startingPosition', 'batch_size': 'batchSize', 'max_batching_window': 'maxBatchingWindow'})
class KinesisEventSourceProps(StreamEventSourceProps):
    def __init__(self, *, starting_position: aws_cdk.aws_lambda.StartingPosition, batch_size: typing.Optional[jsii.Number]=None, max_batching_window: typing.Optional[aws_cdk.core.Duration]=None):
        """
        :param starting_position: Where to begin consuming the stream.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5). Default: Duration.seconds(0)
        """
        self._values = {
            'starting_position': starting_position,
        }
        if batch_size is not None: self._values["batch_size"] = batch_size
        if max_batching_window is not None: self._values["max_batching_window"] = max_batching_window

    @property
    def starting_position(self) -> aws_cdk.aws_lambda.StartingPosition:
        """Where to begin consuming the stream."""
        return self._values.get('starting_position')

    @property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        default
        :default: 100
        """
        return self._values.get('batch_size')

    @property
    def max_batching_window(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5).

        default
        :default: Duration.seconds(0)
        """
        return self._values.get('max_batching_window')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KinesisEventSourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["ApiEventSource", "DynamoEventSource", "DynamoEventSourceProps", "KinesisEventSource", "KinesisEventSourceProps", "S3EventSource", "S3EventSourceProps", "SnsEventSource", "SqsEventSource", "SqsEventSourceProps", "StreamEventSource", "StreamEventSourceProps", "__jsii_assembly__"]

publication.publish()
