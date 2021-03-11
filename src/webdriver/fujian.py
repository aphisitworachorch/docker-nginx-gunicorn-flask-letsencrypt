# FUJIAN Discovery tool for SUT REG
# !Python
import re
from functools import reduce
from operator import mul

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


def getonline_subject(subject_id):
    r = requests.post("http://reg5.sut.ac.th/registrar/examdata/searchexamcourse.asp", data=dict(
        VAPPLICANTCODE=subject_id
    ))
    r.encoding = r.apparent_encoding
    sr = BeautifulSoup(r.text, 'html.parser')
    table_reg = sr.find_all('td')
    subject_list = []
    btn_if = []
    i = 0
    for tb in table_reg:
        btn_if = [x['value'] for x in sr.find_all('input',attrs={'type':'checkbox'})]
        subject_f = tb.find_all('font', attrs={'face': 'MS Sans Serif', 'color': '#000080', 'size': '3'})
        link = [x['href'] for x in tb.find_all('a', href=True)]
        if len(subject_f) <= 0:
            pass
        else:
            subject_list_san = str(re.sub('<.*?>', '', str(subject_f[0])).replace('\xa0', '').rstrip())
            if subject_list_san == 'Link':
                subject_list.append(str(link[0]))
            else:
                subject_list.append(subject_list_san)
            i = i + 1

    shape = [len(subject_list), 9]

    lr = reshape(subject_list, shape)
    subj = []
    for l in lr:
        i = 0
        subj.append({
            "number": l[i + 1],
            "subject": l[i + 2],
            "lecturer": l[i + 4],
            "place": l[i + 3],
            "zoom": l[i + 5],
            "fb": l[i + 7],
            "line": l[i + 8],
            "etc": l[i + 6],
            "mixed": btn_if[i]
        })
        i = i + 1

    return subj


def reshape(lst, shape):
    if len(shape) == 1:
        return lst
    n = reduce(mul, shape[1:])
    return [reshape(lst[i * n:(i + 1) * n], shape[1:]) for i in range(len(lst) // n)]


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
