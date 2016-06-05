#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is used to calculate and plot PR Curve. Plz run after threshold_evaluation.py

from evaluation_summary import summary
import matplotlib.pyplot as plt

stride_length = 5

v_precision_list = []
v_recall_list = []
f_precision_list = []
f_recall_list = []
for i in xrange(0, 11, stride_length):
    threshold = float(i) / 10
    print "Summary threshold {0}...".format(threshold)
    v_precision, v_recall, v_false_rate, f_precision, f_recall, f_false_rate = summary(threshold)
    v_precision_list.append(v_precision)
    v_recall_list.append(v_recall)
    f_precision_list.append(f_precision)
    f_recall_list.append(f_recall)

print 'v_precision_list', v_precision_list
print 'v_recall_list', v_recall_list
print 'f_precision_list', f_precision_list
print 'f_recall_list', f_recall_list

# plot precision-recall
# video evaluation
result_figure = plt.figure('PR Curve')
ax = result_figure.add_subplot(111)
ax.plot(v_recall_list, v_precision_list, 'g', label='video evaluation')
ax.plot(f_recall_list, f_precision_list, 'b', label='frame evaluation')
ax.legend(loc=3)
ax.set_xticks(map(lambda x: float(x) / 10, xrange(-1, 12, 1)))
ax.set_yticks(map(lambda x: float(x) / 10, xrange(-1, 12, 1)))

ax.set_title('PR Curve')
ax.set_xlabel('Recall')
ax.set_ylabel('Precision')
plt.savefig('/home/zjc/log/precison-recall.jpg')
plt.show()
