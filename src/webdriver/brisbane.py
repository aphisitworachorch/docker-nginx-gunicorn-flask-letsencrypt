# FUJIAN Discovery tool for SUT REG
# !Python
import random
from datetime import datetime

import requests
import pandas as pd
import json
from ctypes import cdll, CDLL

cdll.LoadLibrary("libc.so.6")
libc = CDLL("libc.so.6")


class Brisbane:

    def __init__(self, acadyear, semester, levelfrom, levelto, functions=None):
        self.parameters = None
        if functions == "get_student":
            self.parameters = {
                'acadyear': acadyear,
                'semester': semester,
                'levelidfrom': levelfrom,
                'levelidto': levelto
            }
        elif functions == "get_graduate":
            self.parameters = {
                'createdatefrom': '19980101',
                'acadyear': acadyear,
                'semester': semester,
                'createdateto': '20200904',
                'firstdayshowfrom': '1/1/2541',
                'firstdayshowto': '4/9/2563',
                'studentstatusfrom': '40',
                'studentstatusto': '40'
            }

        self.excelGet = requests.get('https://reg5.sut.ac.th/registrar/DataStudentreportInExcel.asp',
                                     params=self.parameters,
                                     stream=True)

    def cloaker(self, object_name, cloak):
        if cloak:
            return ''.join(map(str, random.choices(object_name, k=random.randint(2, len(object_name)))))
        else:
            return object_name

    def string_cutter(self, object_name, cutter):
        if cutter:
            return str(object_name)[:4]
        else:
            return object_name

    def get_student_info(self):
        libc.malloc_trim(0)
        html_body = pd.read_html(self.excelGet.content)
        dataframe = pd.DataFrame(data=html_body[0])
        i = 0
        jsonData = []
        for index, row in dataframe.iterrows():
            if index == 0 or index == 1:
                pass
            else:
                data = {
                    "student_id": self.string_cutter(str(row[1]).replace('"', ''), False),
                    "name": self.cloaker(str(row[2]).replace('"', ''), False),
                    "status": str(row[3]).replace('"', ''),
                    "insert_date": str(row[4]).replace('"', ''),
                    "first_student_id": str(row[1]).replace('"', '')[:3]
                }
                jsonData.append(json.dumps(data))
        return jsonData

    def get_student_graduate(self):
        libc.malloc_trim(0)
        html_body = pd.read_html(self.excelGet.content)
        dataframe = pd.DataFrame(data=html_body[0])
        i = 0
        jsonData = []
        for index, row in dataframe.iterrows():
            if index == 0 or index == 1:
                pass
            else:
                dtx = datetime.strptime(str(row[4]).replace('"', '')[:10], '%d/%m/%Y')
                data = {
                    "student_id": self.string_cutter(str(row[1]).replace('"', ''), False),
                    "name": self.cloaker(str(row[2]).replace('"', ''), False),
                    "status": str(row[3]).replace('"', ''),
                    "success_date": dtx,
                    "first_student_id": str(row[1]).replace('"', '')[:3]
                }
                jsonData.append(json.dumps(data))
        return jsonData

    def getStudentQuantity(self):
        return len(self.get_student_info())
