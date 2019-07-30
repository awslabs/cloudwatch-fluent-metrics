# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging

from .metric import FluentMetric

log = logging.getLogger('metric')
log.addHandler(logging.NullHandler())

# This is defined by CloudWatch
PAGE_SIZE = 20


class BufferedFluentMetric(FluentMetric):
    '''A FluentMetric that tries to buffer as many metrics into as few requests
    as possible. Usage is intended to be exactly the same as FluentMetric, but
    make sure you re-use the BufferedFluentMetric instance (otherwise it won't buffer!)

    Occassionally, you may want to call metric.flush() manually (perhaps at the end of a
    web request or on a timer) to ensure that data is never older than a certain age.

    This class is not thread safe.
    '''

    def __init__(self, client=None, max_items=PAGE_SIZE * 5, **kwargs):
        FluentMetric.__init__(self, client, **kwargs)
        self.max_items = max_items
        self.buffers = {}

    def _record_metric(self, metric_data):
        size = self._size()

        num_allowed = self.max_items - size
        if num_allowed < len(metric_data):
            log.warn("Dropping {} out of {} metrics".format(len(metric_data) - num_allowed, len(metric_data)))

        buffer = self.buffers.get(self.namespace, [])
        self.buffers[self.namespace] = buffer  # in case it wasn't set

        buffer += metric_data[:num_allowed]

        # clear as much WIP as possible
        self.flush(send_partial=False)

    def _size(self):
        return sum([len(buffer) for buffer in self.buffers.values()])

    def flush(self, send_partial=True):
        '''Sends as much data as possible to CloudWatch. If send_partial is set to False,
        this only sends full pages. This way, it minimizes the API usage at the cost of
        delaying data.
        '''
        for namespace, buffer in self.buffers.items():
            full_pages = len(buffer) // PAGE_SIZE
            for i in range(full_pages):
                start = i * PAGE_SIZE
                end = (i + 1) * PAGE_SIZE
                page = buffer[start:end]

                # ship it
                FluentMetric._record_metric(self, page)

            start = full_pages * PAGE_SIZE
            end = len(buffer) % PAGE_SIZE
            if send_partial:
                # ship remaining items
                page = buffer[start:end]
                FluentMetric._record_metric(self, page)

                # clear buffer
                self.buffers[namespace] = []

            # This condition isn't needed for correctness, it could be an else, it just
            # reduces memory churn. You should get the same result either way.
            elif full_pages > 0:
                # clear shipped items from buffer
                self.buffers[namespace] = buffer[start:]

        return self
