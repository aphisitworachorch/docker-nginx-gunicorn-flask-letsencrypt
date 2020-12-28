# FUJIAN Discovery tool for SUT REG
# !Python
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

info = []


def getRandomHeaders():
    ua = UserAgent()
    headers = {'User-Agent': str(ua)}
    return headers


def identifyStudentID(studentid):
    info = dict(number=0, degree="")
    if str(studentid)[0] == "B":
        info["number"] = 1
        info["degree"] = "ปริญญาตรี"
    elif str(studentid)[0] == "M":
        info["number"] = 2
        info["degree"] = "ปริญญาโท"
    elif str(studentid)[0] == "D":
        info["number"] = 3
        info["degree"] = "ปริญญาเอก"
    elif str(studentid)[0] == "A":
        info["number"] = 8
        info["degree"] = "ผู้ร่วมเรียน / สอบเข้าใหม่ / ทดสอบระบบ"
    elif str(studentid)[0] == "C":
        info["number"] = 4
        info["degree"] = "ผู้ร่วมเรียน / สอบเข้าใหม่ / ทดสอบระบบ"
    elif str(studentid)[0] == "G":
        info["number"] = 6
        info["degree"] = "ผู้ร่วมเรียน / สอบเข้าใหม่ / ทดสอบระบบ"
    elif str(studentid)[0] == "I":
        info["number"] = 5
        info["degree"] = "ผู้ร่วมเรียน / สอบเข้าใหม่ / ทดสอบระบบ"
    elif str(studentid)[0] == "V":
        info["number"] = 9
        info["degree"] = "ผู้ร่วมเรียน / สอบเข้าใหม่ / ทดสอบระบบ"
    elif str(studentid)[0] == "X":
        info["number"] = 7
        info["degree"] = "ผู้ร่วมเรียน / สอบเข้าใหม่ / ทดสอบระบบ"
    return info


def fetchall(studentid):
    require_page = 'https://reg.sut.ac.th/registrar/learn_time.asp?studentid=' + str(studentid) + '&f_cmd=2'
    return require_page


def fetchall_eduyear(studentid, eduyear):
    require_page = 'https://reg.sut.ac.th/registrar/learn_time.asp?studentid=' + str(
        studentid) + '&f_cmd=2&acadyear=' + str(eduyear)
    return require_page


def fetchall_eduyear_term(studentid, eduyear, term):
    require_page = 'https://reg.sut.ac.th/registrar/learn_time.asp?studentid=' + str(
        studentid) + '&f_cmd=2&acadyear=' + str(eduyear) + '&maxsemester=' + str(term)
    return require_page


def urlreturn(stdid):
    require_page = 'https://reg.sut.ac.th/registrar/learn_time.asp?studentid=' + str(stdid) + '&f_cmd=2'
    return require_page


def getstudent_name(stdid):
    r = requests.post("https://reg.sut.ac.th/registrar/learn_time.asp", data=dict(
        f_cmd="1",
        f_studentcode=stdid,
        f_studentname="",
        f_studentsurname="",
        f_studentstatus="all",
        departmentid="",
        programid="",
        f_maxrows="25"
    ), headers=getRandomHeaders())
    r.encoding = r.apparent_encoding
    sr = BeautifulSoup(r.text, 'html.parser')

    namet = []
    for mmp in sr.find_all('font', attrs={'face': 'MS Sans Serif', 'size': '3'}):
        namet.append(mmp.find("font").text)

    try:
        mrx = re.sub('<.*?>', '', str(namet[0])).replace('\xa0', '')
        xm = mrx.strip("[]")
    except IndexError:
        xm = "Error To Get"

    return xm


def getstudentenrollment_id(url):
    data_id = []
    page = requests.get(url, headers=getRandomHeaders())
    page.encoding = page.apparent_encoding
    webpage = BeautifulSoup(page.text, 'html.parser')
    table_reg = webpage.find_all('tr', attrs={'valign': 'TOP'})
    for tb in table_reg:
        find_other_step = tb.find('font', attrs={'face': 'MS Sans Serif'})
        data_id.append(regex_sanitize(find_other_step))

    del data_id[0]
    return data_id


def getstudentenrollment_name(url):
    data_name = []
    page = requests.get(url, headers=getRandomHeaders())
    page.encoding = page.apparent_encoding
    webpage = BeautifulSoup(page.text, 'html.parser')
    table_reg = webpage.find_all('tr', attrs={'valign': 'TOP'})
    for tb in table_reg:
        find_other_second_step = tb.find('font', attrs={'face': 'MS Sans Serif', 'size': '2'})
        data_name.append(subject_regex_sanitize(find_other_second_step))

    del data_name[0]
    return data_name


def getstudentenrollment_raw(url):
    page = requests.get(url, headers=getRandomHeaders())
    page.encoding = page.apparent_encoding
    webpage = BeautifulSoup(page.text, 'html.parser')
    web = webpage.find_all('font', attrs={'face': 'MS Sans Serif', 'size': '3'})

    lengthweb = len(web)
    subject = []

    for v in range(lengthweb):
        subject.append(web[v])

    return subject


def subject_regex_sanitize(content):
    st = re.sub('<br.*?>', ' - ', str(content))
    return re.sub('<.*?>', '', str(st)).replace('\xa0', '')


def regex_sanitize(content):
    return re.sub('<.*?>', '', str(content)).replace('\xa0', '')


def getinstitute(content):
    institute = content[5]
    return re.sub('<.*?>', '', str(institute)).replace('\xa0', '')


def getminor(content):
    minor = content[7]
    return re.sub('<.*?>', '', str(minor)).replace('\xa0', '')


def getassistant(content):
    assistant = content[9]
    return re.sub('<.*?>', '', str(assistant)).replace('\xa0', '')


def sanitizehtml(content, lengthweb):
    countenroll = 0
    fullcontent = []
    temp = ""
    sanitizer = ""

    for v in range(11, lengthweb):
        if v % 2 == 0:
            countenroll = countenroll + 1
        temp = content[v]
        sanitizer = re.sub('<.*?>', '', str(temp)).replace('\xa0', '')
        fullcontent.append(sanitizer)

    return fullcontent


def getsanit_subject_without_groupnum(fullcontent):
    vx = 0
    withoutgroupnum = []
    i = 0
    for respond in fullcontent:
        if i % 2 == 0:
            withoutgroupnum.append(respond)
        else:
            vx = vx + 1
        i = i + 1

    return withoutgroupnum
