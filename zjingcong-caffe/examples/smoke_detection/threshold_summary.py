#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is used to calculate and plot PR Curve. Plz run after threshold_evaluation.py

from evaluation_summary import summary
import matplotlib.pyplot as plt

stride_length = 1

v_precision_list = []
v_recall_list = []
v_false_rate_list = []
f_precision_list = []
f_recall_list = []
f_false_rate_list = []
for i in xrange(0, 11, stride_length):
    threshold = float(i) / 10
    print "Summary threshold {0}...".format(threshold)
    v_precision, v_recall, v_false_rate, f_precision, f_recall, f_false_rate = summary(threshold)
    v_precision_list.append(v_precision)
    v_recall_list.append(v_recall)
    v_false_rate_list.append(v_false_rate)

    f_precision_list.append(f_precision)
    f_recall_list.append(f_recall)
    f_false_rate_list.append(f_false_rate)

print 'v_precision_list', v_precision_list
print 'v_recall_list', v_recall_list
print 'v_false_rate_list', v_false_rate_list
print 'f_precision_list', f_precision_list
print 'f_recall_list', f_recall_list
print 'f_false_rate_list', f_false_rate_list

# plot PR Curve
pr_figure = plt.figure('PR Curve')
ax_pr = pr_figure.add_subplot(111)
ax_pr.plot(v_recall_list, v_precision_list, 'go-', label='video evaluation')
ax_pr.plot(f_recall_list, f_precision_list, 'mo-', label='frame evaluation')
ax_pr.legend(loc=3)
ax_pr.set_xticks(map(lambda x: float(x) / 10, xrange(0, 12, 1)))
ax_pr.set_yticks(map(lambda x: float(x) / 10, xrange(0, 12, 1)))

ax_pr.set_title('PR Curve')
ax_pr.set_xlabel('Recall')
ax_pr.set_ylabel('Precision')
plt.savefig('/home/zjc/log/PR.jpg')

# plot ROC Curve
roc_figure = plt.figure('ROC Curve')
ax_roc = roc_figure.add_subplot(111)
ax_roc.plot(v_false_rate_list, v_recall_list, 'go-', label='video evaluation')
ax_roc.plot(f_false_rate_list, f_recall_list, 'mo-', label='frame evaluation')
ax_roc.legend(loc=4)
ax_roc.set_xticks(map(lambda x: float(x) / 10, xrange(-1, 12, 1)))
ax_roc.set_yticks(map(lambda x: float(x) / 10, xrange(0, 12, 1)))

ax_roc.set_title('ROC Curve')
ax_roc.set_xlabel('FPR(False Alarm)')
ax_roc.set_ylabel('TPR(Recall)')
plt.savefig('/home/zjc/log/ROC.jpg')

plt.show()
