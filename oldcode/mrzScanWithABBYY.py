from Error_checker import passportScan
import os
import re
import time
import requests
from datetime import datetime
from ABBYY import CloudOCR


def mrz_scan(source_file, APPID, PWD):
    if (os.path.isfile(source_file) == False):
        raise Exception("file error.")
    ocr_engine = CloudOCR(APPID, PWD)
    input_file = open(source_file, 'rb')
    post_file = {input_file.name: input_file}
    # print("Waiting...")
    time.sleep(0.0001)
    result = ocr_engine.process_and_download(
        post_file, exportFormat='txt', language='English')
    mrz_code = ""
    f = result['txt'].read().decode("utf-8")
    for d in f.splitlines()[-3:]:
        if '<' in d:
            # remove space for error scan
            mrz_code += re.sub(' ', '', d)[:44]
            mrz_code += '\n'
    print("ourcode :", mrz_code)
    return mrz_code


def scanMrzWithPi(pathImg="Pictures/"+datetime.today().strftime('%Y%m%d')+".jpg"):
    APPID = 'ed939c91-9ca3-4b49-be87-f7f666d49c09'
    PWD = 'pH7DLeVLNwPEzEVh4lqTxMqW'
    code = mrz_scan(pathImg, APPID, PWD)
    p1 = passportScan(code)

    # if scan pass
    p1.detail()
    # print(p1.__dict__)
    return p1
