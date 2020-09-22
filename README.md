# FluentMetrics
## **IMPORTANT: When using unique stream IDs, you have the potential to create a large number of metrics. Please make sure to review the [current AWS CloudWatch Custom Metrics pricing]( https://aws.amazon.com/cloudwatch/pricing/) before proceeding.**
## Overview
`FluentMetrics` is an easy-to-use Python module that makes logging CloudWatch custom metrics a breeze. The goal is to provide a framework for logging detailed metrics with a minimal footprint. When you look at your code logic, you want to see your actual code logic, not line after line of metrics logging.  `FluentMetrics` lets you maximize your metrics footprint while minimizing your metrics code footprint.
## Installation
You can install directly from PyPI:

```sh
pip install cloudwatch-fluent-metrics
```
## 'Fluent' . . . what is that?
Fluent describes an easy-to-read programming style. The goal of fluent development is to make code easier to read and reduce the amount of code required to build objects. It's easier to take a look a comparison between fluent and non-fluent style.
#### Non-Fluent Example
```sh
g = Game()
f = Frame(Name='Tom')
f.add_score(7)
f.add_score(3)
g.add_frame(f)
f = Frame(Name='Tom')
f.add_strike()
g.add_frame(f)
```
#### Non-Fluent Example with Constructor
```sh
g = Game()
g.add_frame(Frame(Name='Tom', Score1=7, Score2=3)
g.add_frame(Frame(Name='Tom', Score1=10)
```
#### Fluent Example
```sh
g = Game()
g.add_frame(Frame().with_name('Tom').score(3).spare())
g.add_frame(Frame().with_name('Tom').strike())
```
While the difference may seem to be nitpicking, a frame is really just a constructed object. In the first example, we're taking up three lines of code to create the object--there's nothing wrong with that. However, in the second example, we're using constructors. This is slightly more readable, but there's a great deal of logic bulked up in our constructor. In the third example, we're using fluent-style code as it starts at creating the frame and *fluently* continues until it's created the entire frame in a single line. And more importantly, *it's readable.* We're not just creating an object with a massive constructor or spending several lines of code just to create a single object.
## Terminology Quickstart
#### Namespaces
Every metric needs to live in a namespace. Since you are logging your own custom metrics, you need to provide a custom namespace for your metric. Click [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-namespaces.html) for a list of the standard AWS namespaces.
*Example*:
In this example, we're creating a simple `FluentMetric` in a namespace called `Performance`. This means that every time we log a metric with `m`, we will automatically log it to the `Performance` namespace.
```sh
from fluentmetrics import FluentMetric
m = FluentMetric().with_namespace('Performance')
```
#### Metric Names
The metric name is the thing you are actually logging. Each value that you log must be tied to a metric name. When you log a custom metric with a new metric name, the name will automatically be created if it doesn't already exist. Click [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/viewing_metrics_with_cloudwatch.html) to see existing metrics that can help you define names for your custom metrics.
*Example*:
In this example, we're logging two metrics called `StartupTime` and `StuffTime` to the `Performance` namespace (we only needed to define the namespace once).
```sh
m = FluentMetric().with_namespace('Performance')
m.log(MetricName='StartupTime', Value=27, Unit='Seconds')
do_stuff()
m.log(MetricName='StuffTime', Value=12000, Unit='Milliseconds')
```
#### Values
Obviously we need to log a value with each metric. This needs to be a number since we convert this value to a `float` before sending to CloudWatch. 
**IMPORTANT**: When logging multiple values for the same custom metric within a minute, CloudWatch aggregates an average over a minute. Click [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html#publishingDataPoints) for more details.
#### Storage Resolution
The PutMetricData function now accepts an optional StorageResolution parameter. Set this parameter to 1 to publish high-resolution metrics; omit it (or set it to 60) to publish at standard 1-minute resolution.
*Example*:
In this example, we're logging metric at one-second resolution:
```sh
m = FluentMetric().with_namespace('Application/MyApp')
                  .with_storage_resolution(1)
m.log(MetricName='Transactions/Sec', Value=trans_count, Unit='Count/Sec')
```
#### Dimensions
A dimension defines how you want to slice and dice the metric. These are simply name-value pairs and you can define up to 10 per metric. Click [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html#usingDimensions) for more details on using dimensions.
**IMPORTANT:** When you define multiple dimensions, CloudMetrics attaches all of those dimensions to the metric as a single combined dimension set--think of them as an aggregate primary key. For example, if you log a metric with the dimensions `os = 'linux'` and `flavor='ubunutu'` you will only be able to aggregate by **both** `os` and `flavor`. You **cannot** aggregate only by just `os` or just `flavor`. `FluentMetrics` solves this problem by automatically logging three metrics--one for `os`, one for `flavor` and then one for the combied dimensions, giving you maximum flexibility.
*Example*:
In this example, we're logging boot/restart time metrics. When this code executes, we will end up with 6 metrics:
* `BootTime` and `RestartTime` for `os`
* `BootTime` and `RestartTime` for `instance-id`
* `BootTime` and `RestartTime` for 'os` and `instance-id`
```sh
m = FluentMetric().with_namespace('Performance/EC2') \
                  .with_dimension('os', 'linux'). \
                  .with_dimension('instance-id', 'i-123456')
boot_time = start_instance()
m.log(MetricName='BootTime', Value=boot_time, Unit='Milliseconds')
restart_time = restart_instance()
m.log(MetricName='RestartTime', Value=restart_time, Unit='Milliseconds')
```
#### Units
CloudWatch has built-in logic to provide meaning to the metric values. We're not just logging a value--we're logging a value of some unit. By defining the unit type, CloudWatch will know how to properly present, aggregate and compare that value with other values. For example, if you submit a value with unit `Milliseconds`, then it can properly aggregate it up to seconds, minutes or hours. This is a list of the most current valid list of units. A more up-to-date list should be available [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html) under the **Unit** section,.
```sh
"Seconds"|"Microseconds"|"Milliseconds"|"Bytes"|"Kilobytes"|"Megabytes"|
"Gigabytes"|"Terabytes"|"Bits"|"Kilobits"|"Megabits"|"Gigabits"|"Terabits"|
"Percent"|"Count"|"Bytes/Second"|"Kilobytes/Second"|"Megabytes/Second"|
"Gigabytes/Second"|"Terabytes/Second"|"Bits/Second"|"Kilobits/Second"|
"Megabits/Second"|"Gigabits/Second"|"Terabits/Second"|"Count/Second"|"None"
```
##### Unit Shortcut Methods
If you don't want to type out the individual unit name, there are shortcut methods for each unit.

```sh
m = FluentMetric().with_namespace('Performance/EC2') \
                  .with_dimension('os', 'linux'). \
                  .with_dimension('instance-id', 'i-123456')
m.seconds(MetricName='CompletionInSeconds', Value='1000')
m.microseconds(MetricName='CompletionInMicroseconds', Value='1000')
m.milliseconds(MetricName='CompletionInMilliseconds', Value='1000')
m.bytes(MetricName='SizeInBytes', Value='1000')
m.kb(MetricName='SizeInKb', Value='1000')
m.mb(MetricName='SizeInMb', Value='1000')
m.gb(MetricName='SizeInGb', Value='1000')
m.tb(MetricName='SizeInTb', Value='1000')
m.bits(MetricName='SizeInBits', Value='1000')
m.kbits(MetricName='SizeInKilobits', Value='1000')
m.mbits(MetricName='SizeInMegabits', Value='1000')
m.gbits(MetricName='SizeInGigabits', Value='1000')
m.tbits(MetricName='SizeInTerabits', Value='1000')
m.pct(MetricName='Percent', Value='20')
m.count(MetricName='ItemCount', Value='20')
m.bsec(MetricName='BandwidthBytesPerSecond', Value='1000')
m.kbsec(MetricName='BandwidthKilobytesPerSecond', Value='1000')
m.mbsec(MetricName='BandwidthMegabytesPerSecond', Value='1000')
m.gbsec(MetricName='BandwidthGigabytesPerSecond', Value='1000')
m.tbsec(MetricName='BandwidthTerabytesPerSecond', Value='1000')
m.bitsec(MetricName='BandwidthBitsPerSecond', Value='1000')
m.kbitsec(MetricName='BandwidthKilobitsPerSecond', Value='1000')
m.mbitsec(MetricName='BandwidthMegabitsPerSecond', Value='1000')
m.gbitsec(MetricName='BandwidthGigabitsPerSecond', Value='1000')
m.tbitsec(MetricName='BandwidthTerabitsPerSecond', Value='1000')
m.countsec(MetricName='ItemCountsPerSecond', Value='1000')
```
#### Timers
One of the most common uses of logging is measuring performance. FluentMetrics allows you to activate multiple built-in timers by name and log the elapsed time in a single line of code. **NOTE:** The elapsed time value is automatically stored as unit `Milliseconds`.
*Example*:
In this example, we're starting timers `workflow` and `job1` at the same time. Timers start as soon as you create them and never stop running. When you call `elapsed`, `FluentMetrics` will log the number of elapsed milliseconds with the `MetricName`.
```sh
m = FluentMetric()
m.with_timer('workflow').with_timer('job1')
do_job1()
m.elapsed(MetricName='Job1CompletionTime', TimerName='job1')
m.with_timer('job2')
do_job2()
m.elapsed(MetricName='Job2CompletionTime', TimerName='job2')
finish_workflow()
m.elapsed(MetricName='WorkflowCompletionTime', TimerName='workflow')
```
#### Metric Stream ID
A key feature of `FluentMetrics` is the metric stream ID. This ID will be added as a dimension and logged with every metric. The benefit of this dimension is to provide a distinct stream of metrics for an end-to-end operation. When you create a new instance of `FluentMetric`, you can either pass in your own value or `FluentMetrics` will generate a GUID. In CloudWatch, you can then see all of the metrics for a particular stream ID in chronological order. A metric stream can be a job, or a server or any way that you want to unique group a contiguous stream of metrics.
*Example*:
In this example, we'll have two metrics in the `Performance` namespace, each with metric stream ID of `abc-123`. We can then go to CloudWatch and filter by that stream ID to see the entire operation performance at a glance.
```sh
m = FluentMetric().with_namespace('Performance').with_stream_id('abc-123')
m.log(MetricName='StartupTime', Value=100, Unit='Seconds')
do_work()
m.log(MetricName='WorkCompleted', Value=1000, Unit='Milliseconds')
```
## Use Case Quickstart
#### #1: Least Amount of Code Required to Log a Metric
This is the minimal amount of work you need to log--create a `FluentMetric` with a namespace, then log a value.
**Result**: This code will log a single value `100` for `ActiveServerCount` in the `Stats` namespace.
```sh
from fluentmetrics import FluentMetric
m = FluentMetric().with_namespace('Stats')
m.log(MetricName='ActiveServerCount', Value='100', Unit='Count')
```
#### #2: Logging Multiple Metrics to the Same Namespace
If you are logging multiple metrics to the same namespace, this is a great use case for `FluentMetrics`. You only need to create one instance of `FluentMetric` and specify a different metric name when you call `log`. 
**Result**: This code will log a single value `100` for `ActiveServerCount` in the `Stats` namespace.
```sh
from fluentmetrics import FluentMetric   
m = FluentMetric().with_namespace('Stats')
m.log(MetricName='ActiveServerCount', Value='10', Unit='Count') \
 .log(MetricName='StoppedServerCount', Value='20', Unit='Count') \
 .log(MetricName='ActiveLinuxCount', Value='50', Unit='Count') \
 .log(MetricName='ActiveWindowsCount', Value='50', Unit='Count')
````
#### #3: Logging Counts
In the previous example, we logged a metric and identified the unit `Count`. Instead of specifying the unit, you can specify the type of object
**Result**: This code will log a single value `100` for `ActiveServerCount` in the `Stats` namespace.

```sh
from fluentmetrics import FluentMetric
m = FluentMetric().with_namespace('Stats')
m.count(MetricName='ActiveServerCount', Value='10')
```

#### BufferedFluentMetric
Normally, with FluentMetric, metrics are sent immediately when `log` is called (or `count`, `milliseconds`, etc). This
can result in a lot of `put_metric_data` calls to CloudWatch that are not full. When you use `BufferedFluentMetric` 
instead of `FluentMetric`, it waits until it has the maximum (20) metrics before calling `put_metric_data`. This optimizes
traffic to cloudwatch.

In general, `BufferedFluentMetric` behaves identically to `FluentMetric`, except that now it is possible to "forget" to
send some metrics. The `BufferedFluentMetric.flush()` method pushes out all metrics immediately (clears the buffer). It
is often best to do this at the end of a request (or some other obviously bounded interval).

Here is an example of how it works in Flask:

```python
from flask import g
from fluentmetrics import BufferedFluentMetric

@app.before_request
def start_request():
	g.metrics = BufferedFluentMetric()
	g.metrics.with_namespace('MyApp')
	g.metrics.with_timer('RequestLatency')

@app.after_request
def end_request(response):
	def error_counter(hundred):
		if response.status_code / 100 == hundred:
			return 1
		else:
			return 0

	g.metrics.count(MetricName='4xxError', Value=error_counter(400))
	g.metrics.count(MetricName='5xxError', Value=error_counter(500))
	g.metrics.count(MetricName='Availability', Value=(1 - error_counter(500)))
	g.metrics.elapsed(MetricName='RequestLatency', TimerName='RequestLatency')

	# Finally, ensure that all metrics end up in CloudWatch before this request finally ends.
	g.metrics.flush()
```

## License

This library is licensed under the Apache 2.0 License. 
