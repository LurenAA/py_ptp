#! /usr/bin/python3
# coding=utf-8

import sys
import subprocess as sp
import os
import re
from pathlib import Path
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker  
from typing import Final

def initialize_matplotlib():
    global plt
    plt.figure(figsize=(11, 6), dpi=500)
    plt.axis([0, 1000, 0, 0.003])
    plt.gca().set_xlabel('Number of measurements', fontsize=12)
    plt.gca().set_ylabel('Time Offset', fontsize= 12)
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.4f s'))
    plt.title('Measure Time Offset')
    plt.grid(True)
    plt.tight_layout()

data_list = []
with open("./dio_ptpd_data") as fd:
    for line in fd:
        data_list.append(float(line[:-2]))
        if(len(data_list) == 1000):
            break
initialize_matplotlib()
plt.scatter(np.arange(0,1000,1), data_list, c= ['#17becf'],alpha=0.8, label="fc ptpd with dio", marker=".")
plt.legend()
# plt.savefig("./r/dio_fc_ptpd")

data_list2 = []
with open("./2fc_ptpd_data") as fd:
    for line in fd:
        data_list2.append(float(line[:-2]))
        if(len(data_list2) == 1000):
            break
# plt.clf()
# initialize_matplotlib()
plt.scatter(np.arange(0,1000,1), data_list2, c= ['#ff7f0e'],alpha=0.8, label="fc ptpd without dio", marker=".")
plt.legend()
# plt.savefig("./r/ndio_fc_ptpd")
plt.savefig("./r/compare_ptpd")