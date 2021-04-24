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

class StatusConstant:
    NONE:Final = 0
    NTP: Final = 0x01
    PTPD: Final = 0x02
    FCPTPD: Final = 0x04
    ALL: Final = 0x10
    #result picture file position
    NTP_PATH: Final = './r/ntp'   
    FCPTPD_PATH: Final = './r/fcptpd'
    PTPD_PATH: Final = './r/ptpd'  
    ALL_PATH: Final = './r/all'
    #where read data from 
    NTP_DATA_PATH: Final = '/home/xgb/py_ptp/ntp_data'
    FCPTPD_DATA_PATH: Final = '/home/xgb/py_ptp/fc_ptp_data'
    PTPD_DATA_PATH: Final = "/home/xgb/py_ptp/ptpd_data"

class Status(StatusConstant):
    '''target Status class'''
    __target_status = StatusConstant.NONE
    __ntp_path = StatusConstant.NTP_PATH
    __ntp_data_path = StatusConstant.NTP_DATA_PATH
    __fc_ptpd_data_path = StatusConstant.FCPTPD_DATA_PATH
    __fc_ptpd_path = StatusConstant.FCPTPD_PATH
    __ptpd_path = StatusConstant.PTPD_PATH
    __ptpd_data_path = StatusConstant.PTPD_DATA_PATH
    __all_path = StatusConstant.ALL_PATH
    @staticmethod
    def __check(n: int, m: int) -> bool:
        return 0xff & n & m
    @staticmethod
    def __set(n: int) -> None:
        Status.__target_status |= n
    #check status
    @staticmethod
    def CHECK_NTP() -> bool: 
        return Status.__check(Status.NTP, Status.__target_status)
    @staticmethod
    def CHECK_ALL() -> bool:
        return Status.__check(Status.ALL, Status.__target_status)
    @staticmethod
    def CHECK_PTPD() -> bool:
        return Status.__check(Status.PTPD, Status.__target_status)
    @staticmethod
    def CHECK_FCPTPD() -> bool:
        return Status.__check(Status.FCPTPD, Status.__target_status)
    #set status
    @staticmethod
    def SET_NTP() -> None:
        Status.__set(Status.NTP)
    @staticmethod
    def SET_ALL() -> None:
        Status.__set(Status.ALL)
    @staticmethod
    def SET_PTPD() -> None:
        Status.__set(Status.PTPD)
    @staticmethod
    def SET_FCPTPD() -> None:
        Status.__set(Status.FCPTPD)
    #set/get result path
    @staticmethod
    def SET_NTP_PATH(s: str) -> None:
        Status.__ntp_path = s
    @staticmethod
    def GET_NTP_PATH() -> str:
        return Status.__ntp_path
    @staticmethod
    def SET_FC_PTPD_PATH(s: str) -> None:
        Status.__fc_ptpd_path = s
    @staticmethod
    def GET_FC_PTPD_PATH() -> str:
        return Status.__fc_ptpd_path
    @staticmethod
    def GET_PTPD_PATH() -> str :
        return Status.__ptpd_path
    @staticmethod
    def SET_PTPD_PATH(s: str) -> None:
        Status.__ptpd_path = str
    @staticmethod
    def SET_ALL_PATH(s: str) -> None:
        Status.__all_path = s
    @staticmethod
    def GET_ALL_PATH() -> str:
        return Status.__all_path
    #set/get data path
    @staticmethod
    def GET_NTP_DATA_PATH() ->str:
        return Status.__ntp_data_path
    @staticmethod
    def SET_NTP_DATA_PATH(s: str)-> None:
        Status.__ntp_data_path = s
    @staticmethod
    def SET_FC_PTPD_DATA_PATH(s: str) -> None:
        Status.__fc_ptpd_data_path = s
    @staticmethod
    def GET_FC_PTPD_DATA_PATH() -> str:
        return Status.__fc_ptpd_data_path
    @staticmethod
    def SET_PTPD_DATA_PATH(s: str) -> None:
        Status.__ptpd_data_path = s
    @staticmethod
    def GET_PTPD_DATA_PATH() -> str:
        return Status.__ptpd_data_path


def initialize_matplotlib():
    global plt
    plt.figure(figsize=(11, 6), dpi=500)
    plt.axis([0, 1000, 0, 0.003])
    plt.gca().set_xlabel('Number of measurements', fontsize=12)
    plt.gca().set_ylabel('Time Offset', fontsize= 12)
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f s'))
    plt.title('Measure Time Offset')
    plt.grid(True)
    plt.tight_layout()

argv = sys.argv
help_options = '''\
Usage: tpf OPTION...
Options and arguments:
 -a, --all        \ttarget all 
 -n, --ntp        \ttarget ntp
 -p, --ptpd       \ttarget ptpd
 -c, --fc_ptpd    \ttarget fc ptpd
 -h, --help       \tgive this help list
 -nf=file_path    \twhere to read ntp data file(default to /home/xgb/py_ptp/ntp_data)
                  \t  (if file no exist, query the data,make sure ntp has started)
 -cf=file_path    \twhere to read fc ptpd data file(default to /home/xgb/py_ptp/fc_ptp_data)
 -pf=file_path    \twhere to read ptpd data file(default to /home/xgb/py_ptp/ptpd_data)  
 -nt=file_path    \twhere to put result ntp picture file(./r/ntp)
 -ct=file_path    \twhere to put result fc ptp picture file(./r/fcptpd) 
 -pt=file_path    \twhere to put result ptpd picture file(./r/ptpd)
 -at=file_path    \twhere to put comparision picture file(./r/all)
'''

if(len(argv) == 1):
    print("Error: No options")
    print(help_options)
    exit()

for element in argv[1:]:
    if(element == "-h" or element == "--help"):
        print(help_options)
        exit()
    elif(element == '-n' or element == '--ntp'):
        Status.SET_NTP()
    elif(element == '-a' or element == '--all'):
        Status.SET_ALL()
    elif(element == '-p' or element == '--ptpd'):
        Status.SET_PTPD()
    elif(element == '-c' or element == '--fc_ptpd'):
        Status.SET_FCPTPD()
    elif(element[:3] == "-nf"):
        Status.SET_NTP_DATA_PATH(element[4:])
    elif(element[:3] == '-cf'):
        Status.SET_FC_PTPD_DATA_PATH(element[4:])
    elif(element[:3] == '-pf'):
        Status.SET_PTPD_DATA_PATH(element[4:])
    elif(element[:3] == '-nt'):
        Status.SET_NTP_PATH(element[4:])
    elif(element[:3] == '-ct'):
        Status.SET_FC_PTPD_PATH(element[4:])
    elif(element[:3] == '-pt'):
        Status.SET_PTPD_PATH(element[4:])
    elif(element[:3] == 'at'):
        Status.SET_ALL_PATH(element[4:])
    else:
        print("Error:undefined Options")
        print(help_options)
        exit()

initialize_matplotlib()
if(Status.CHECK_NTP()) :
    data_list = []
    ntp_data = Path(Status.GET_NTP_DATA_PATH())
    if(not ntp_data.is_file()):
        print('wait for get ntp data.....')
        for i in range(1000):
            prs = sp.run(['ntpdate','-q', 'xgb_target'], capture_output  = True, check=True)
            # print(prs.stdout.decode('utf-8'))
            reo = re.compile("(?<=offset )[^,]*")
            res = reo.search(prs.stdout.decode('utf-8'))
            data_list.append(float(res.group(0)))
            # print(res.group(0))
        # print(data_list)
        with open(Status.GET_NTP_DATA_PATH(), 'x') as fd:
            json.dump(data_list ,fd)
    else:
        with open(Status.GET_NTP_DATA_PATH()) as fd:
            data_list = json.load(fd)
    # print(data_list)
    plt.scatter(np.arange(0,1000,1), data_list, alpha=0.8, label="ntp", marker=".")
    plt.legend()
    if(not Status.CHECK_ALL()):
        plt.savefig(Status.GET_NTP_PATH())

if(Status.CHECK_FCPTPD()):
    data_list = []
    fc_ptp_data = Path(Status.GET_FC_PTPD_DATA_PATH())
    if(not fc_ptp_data.is_file()):
        print("Error: no fc ptpd data file\n")
        print(help_options)
        exit()
    with open(Status.GET_FC_PTPD_DATA_PATH()) as fd:
        for line in fd:
            data_list.append(float(line[:-2]))
            if(len(data_list) == 1000):
                break
    if(not Status.CHECK_ALL()):
        plt.clf()
        initialize_matplotlib()
    plt.scatter(np.arange(0,1000,1), data_list, c= ['#ff7f0e'],alpha=0.8, label="fc ptpd", marker=".")
    plt.legend()
    if(not Status.CHECK_ALL()):
        plt.savefig(Status.GET_FC_PTPD_PATH())

if(Status.CHECK_PTPD()):
    data_list = []
    ptpd_data = Path(Status.GET_PTPD_DATA_PATH())
    if(not ptpd_data.is_file()):
        print("Error: no ptpd data file\n")
        print(help_options)
        exit() 
    with open(Status.GET_PTPD_DATA_PATH()) as fd:
        for line in fd:
            data_list.append(float(line[:-2]))
            if(len(data_list) == 1000):
                break
    if(not Status.CHECK_ALL()):
        plt.clf()
        initialize_matplotlib()
    plt.scatter(np.arange(0,1000,1), data_list, c= ['#17becf'],alpha=0.8, label="ptpd", marker=".")
    plt.legend()
    if(not Status.CHECK_ALL()):
        plt.savefig(Status.GET_PTPD_PATH())

if(Status.CHECK_ALL()) :
    plt.savefig(Status.GET_ALL_PATH())