# FUJIAN Discovery tool for SUT REG
# !Python
import requests
import pandas as pd
import json


class Brisbane:

    def __init__(self, acadyear, semester, levelfrom, levelto):
        self.excelGet = requests.get(
            'https://reg5.sut.ac.th/registrar/DataStudentreportInExcel.asp?acadyear=' + str(acadyear) + '&semester=' + str(semester) + '&levelidfrom=' +
            str(levelfrom) + '&levelidto=' + str(levelto),
            stream=True)

    def get(self):
        html_body = pd.read_html(self.excelGet.content)
        dataframe = pd.DataFrame(data=html_body[0])
        i = 0
        jsonData = {}
        for index, row in dataframe.iterrows():
            if index == 0 or index == 1:
                pass
            else:
                data = {
                    "student_id": str(row[1]).replace('"', ''),
                    "name": str(row[2]).replace('"', ''),
                    "status": str(row[3]).replace('"', ''),
                    "insert_date": str(row[4]).replace('"', ''),
                    "first_student_id": str(row[1]).replace('"', '')[:3],
                    "fujian_url": str("https://cloud.arsanandha.xyz/student/") + str(row[1]).replace('"', '')
                }
                jsonData.update(data)
        return jsonData

    def getStudentQuantity(self):
        return len(self.get())
