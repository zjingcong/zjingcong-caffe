#!/usr/bin/env python
# -*- coding: utf-8 -*-

from test_result_evaluation import result_evaluation

for i in xrange(0, 11):
    threshold = float(i) / 10
    result_evaluation(threshold)
