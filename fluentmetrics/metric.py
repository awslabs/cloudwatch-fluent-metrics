# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

#    http://aws.amazon.com/asl/

# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and limitations under the License.

import logging
import arrow
import uuid
import boto3
import boto3.session

logger = logging.getLogger('metric')
logger.addHandler(logging.NullHandler())


class Timer(object):
    def __init__(self):
        self.start = arrow.utcnow()

    def elapsed(self):
        return arrow.utcnow() - self.start

    def elapsed_in_ms(self):
        return self.elapsed().total_seconds() * 1000

    def elapsed_in_seconds(self):
        return self.elapsed().total_seconds()


class FluentMetric(object):
    def __init__(self, client=None, Profile=None):
        self.stream_id = str(uuid.uuid4())
        self.dimensions = []
        self.timers = {}
        self.dimension_stack = []
        self.storage_resolution = 60
        self.with_dimension('MetricStreamId', self.stream_id)

        if client:
            self.client = client
        else:
            profile = Profile
            if profile:
                session = boto3.session.Session(profile_name=profile)
                self.client = session.client('cloudwatch')
            else:
                self.client = boto3.client('cloudwatch')

    def with_storage_resolution(self, value):
        self.storage_resolution = value
        return self

    def with_stream_id(self, id):
        self.stream_id = id
        self.with_dimension('MetricStreamId', self.stream_id)
        return self

    def with_namespace(self, namespace):
        self.namespace = namespace
        return self

    def with_dimension(self, name, value):
        self.without_dimension(name)
        self.dimensions.append({'Name': name, 'Value': value})
        return self

    def without_dimension(self, name):
        if not self.does_dimension_exist(name):
            return
        self.dimensions = \
            [item for item in self.dimensions if not item['Name'] == name]
        return self

    def does_dimension_exist(self, name):
        d = [item for item in self.dimensions if item['Name'] == name]
        if d:
            return True
        else:
            return False

    def get_dimension_value(self, name):
        d = [item for item in self.dimensions if item['Name'] == name]
        if d:
            return d[0]['Value']
        else:
            return None

    def with_timer(self, timer):
        self.timers[timer] = Timer()
        return self

    def without_timer(self, timer):
        if timer in self.timers.keys():
            del self.timers[timer]
        return self

    def get_timer(self, timer):
        if timer in self.timers.keys():
            return self.timers[timer]
        else:
            return None

    def push_dimensions(self):
        self.dimension_stack.append(self.dimensions)
        self.dimensions = []
        self.with_stream_id(self.stream_id)
        return self

    def pop_dimensions(self):
        self.dimensions = self.dimension_stack.pop()
        return self

    def elapsed(self, MetricName, TimerName=None):
        TimerName = TimerName or MetricName
        if TimerName not in self.timers.keys():
            logger.warn('No timer named {}'.format(TimerName))
            return
        self.log(Value=self.timers[tn].elapsed_in_ms(),
                 Unit='Milliseconds',
                 MetricName=MetricName)
        return self

    def countsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Count/Second',
                 MetricName=MetricName)
        return self

    def tbitsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Terabits/Second',
                 MetricName=MetricName)
        return self

    def gbitsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Gigabits/Second',
                 MetricName=MetricName)
        return self

    def mbitsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Megabits/Second',
                 MetricName=MetricName)
        return self

    def kbitsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Kilobits/Second',
                 MetricName=MetricName)
        return self

    def bitsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Bits/Second',
                 MetricName=MetricName)
        return self

    def tbsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Terabytes/Second',
                 MetricName=MetricName)
        return self

    def gbsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Gigabytes/Second',
                 MetricName=MetricName)
        return self

    def mbsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Megabytes/Second',
                 MetricName=MetricName)
        return self

    def kbsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Kilobytes/Second',
                 MetricName=MetricName)
        return self

    def bsec(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Bytes/Second',
                 MetricName=MetricName)
        return self

    def pct(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Percent',
                 MetricName=MetricName)
        return self

    def tbits(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Terabits',
                 MetricName=MetricName)
        return self

    def gbits(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Gigabits',
                 MetricName=MetricName)
        return self

    def mbits(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Megabits',
                 MetricName=MetricName)
        return self

    def kbits(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Kilobits',
                 MetricName=MetricName)
        return self

    def bits(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Bits',
                 MetricName=MetricName)
        return self

    def tb(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Terabytes',
                 MetricName=MetricName)
        return self

    def gb(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Gigabytes',
                 MetricName=MetricName)
        return self

    def mb(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Megabytes',
                 MetricName=MetricName)
        return self

    def kb(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Kilobytes',
                 MetricName=MetricName)
        return self

    def bytes(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Bytes',
                 MetricName=MetricName)
        return self

    def milliseconds(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Milliseconds',
                 MetricName=MetricName)
        return self

    def microseconds(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Microseconds',
                 MetricName=MetricName)
        return self

    def seconds(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Seconds',
                 MetricName=MetricName)
        return self

    def count(self, MetricName, Value=1):
        self.log(Value=Value,
                 Unit='Count',
                 MetricName=MetricName)
        return self

    def log(self, MetricName, Value, Unit, TimeStamp=None):
        ts = TimeStamp or arrow.utcnow()
        ts = ts.format('YYYY-MM-DD HH:mm:ss ZZ')
        value = float(Value)
        md = []
        for dimension in self.dimensions:
            md.append({
                        'MetricName': MetricName,
                        'Dimensions': [dimension],
                        'Timestamp': ts,
                        'Value': value,
                        'Unit': Unit,
                        'StorageResolution': self.storage_resolution,
                    }
            )

        md.append({
                    'MetricName': MetricName,
                    'Dimensions': self.dimensions,
                    'Timestamp': ts,
                    'Value': value,
                    'Unit': Unit,
                    'StorageResolution': self.storage_resolution,
                  })

        self._record_metric(md)
        return self

    def _record_metric(self, metric_data):
        logger.debug('log: {}'.format(metric_data))
        self.client.put_metric_data(
            Namespace=self.namespace,
            MetricData=metric_data,
        )

    def get_metrics(self, MetricName):
        return self.client.list_metrics(Namespace=self.namespace,
                                        MetricName=MetricName)['Metrics']
