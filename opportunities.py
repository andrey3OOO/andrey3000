import re
from datetime import date

import pyodbc
from bs4 import BeautifulSoup
from selenium import webdriver

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=AGLAPTOP\SQLEXPRESS;'
                      'Database=db;'
                      'Trusted_Connection=yes;')

sites = ["https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&search=BI",
         "https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&search=Business+Intelligence",
         "https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&descr=1&search=SSRS",
         "https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&search=qlikview&descr=1",
         "https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&search=qlik&descr=1"]
description = ['BI', 'Business Intelligence', 'SSRS', 'qlikview', 'qlik']

driver = webdriver.Chrome("C:/Downloads/chromedriver.exe")

for y, x in zip(sites, description):
    driver.get(y)
    res = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(res, "html.parser")
    douclass = soup.find(class_='b-inner-page-header')
    doudiv = douclass.find('h1')
    name = doudiv.contents[0]
    m = re.sub("\D", "", name)
    today = date.today()
    print(str(m) + ',' + str(x))

    cursor = conn.cursor()

    SQLCommand = ("set nocount on; INSERT INTO dbo.opp ([Date],[Count],[Type]) VALUES (?,?,?)")
    Values = [str(today), str(m), str(x)]
    # Processing Query
    cursor.execute(SQLCommand, Values)
    conn.commit()
    print("Data Successfully Inserted to SQL")

    with open('C:\Downloads\data.csv', 'a') as f:
        f.write(str(today) + ',' + str(m) + ',' + str(x))
        f.write("\n")
conn.close()
driver.quit()

##bla
