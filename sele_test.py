from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import csv
import re

def initializeCsv():
    tags = ["title",
            "instructor",
            "organization",
            "assignments",
            "overall rating",
            "challenge",
            "workload",
            "requirement",
            "expected grade",
            "expected grade P/F",
            "response count"]

    f = open("test.csv", "w+")
    f.truncate()
    f.close()

    with open("test.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(tags)



def writeCsvFile(fname, data):
    """
    @param fname: string, name of file to write
    @param data: list of list of items

    Write data to file
    """
    with open(fname, "a") as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def findCRNs(keyword):
    if keyword == "dist 1":
        driver.get("https://courses.rice.edu/admweb/!SWKSCAT.cat?p_action=QUERY&p_term=201910"
                   "&p_ptrm=&p_crn=&p_onebar=&p_mode=AND&p_subj_cd=&p_subj=&p_dept="
                   "&p_school=&p_spon_coll=&p_df=GRP1&p_insm=&p_submit=")
    if keyword == "dist 2":
        driver.get("https://courses.rice.edu/admweb/!SWKSCAT.cat?p_action=QUERY&p_term=201910"
                   "&p_ptrm=&p_crn=&p_onebar=&p_mode=AND&p_subj_cd=&p_subj=&p_dept="
                   "&p_school=&p_spon_coll=&p_df=GRP2&p_insm=&p_submit=")
    if keyword == "dist 3":
        driver.get("https://courses.rice.edu/admweb/!SWKSCAT.cat?p_action=QUERY&p_term=201910"
                   "&p_ptrm=&p_crn=&p_onebar=&p_mode=AND&p_subj_cd=&p_subj=&p_dept="
                   "&p_school=&p_spon_coll=&p_df=GRP3&p_insm=&p_submit=")

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    crns = []

    for line in soup.findAll('td', {'class' : 'cls-crn'}):
        crns.append(re.split("[<>]", line.renderContents())[2])

    return crns


def getData(soup):
    line = []
    line.append(soup.findAll('span', {'id': 'lblTitle'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblInstructor'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblClassMean1'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblClassMean2'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblClassMean3'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblClassMean4'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblClassMean5'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblClassMean6'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblClassMean7'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblClassMean8'})[0].renderContents())
    line.append(soup.findAll('span', {'id': 'lblResponses1'})[0].renderContents())

    for idx in range(2, len(line)):
        line[idx] = re.findall("[\d\.]+", line[idx])[0]

    return line

usr = raw_input("username: ")
pwd = raw_input("password: ")

dist = "dist 2"

driver = webdriver.Chrome()
crn_list = findCRNs(dist)
# or you can use Chrome(executable_path="/usr/bin/chromedriver")
driver.get("https://scheduleplanner.rice.edu/wsSchedule/Account/CourseSelection.aspx")
# assert "Schedule" in driver.title
elem = driver.find_element_by_id("username")
elem.send_keys(usr)
elem = driver.find_element_by_id("password")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)

data = []


term = "201910"

for crn in crn_list:
    script = ("window.location.replace('./CourseEvalsNew.aspx?H='+" + crn + "+ '&T=' +" + term +
              ",'mywin','left=20,top=20,width=1024,height=950,toolbar=1,resizable=1,scrollbars=1')")

    driver.execute_script("return " + script)

    # driver.get("https://scheduleplanner.rice.edu/wsSchedule/Account/CourseEvalsNew.aspx?H=20993&T=201810")

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    try:
        data.append(getData(soup))
    except (IndexError):
        continue


initializeCsv()
# writeCsvFile(dist + '.csv', data)
writeCsvFile('test.csv', data)


driver.close()