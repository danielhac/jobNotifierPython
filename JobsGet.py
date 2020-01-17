from __future__ import print_function # Python 2/3 compatibility
import boto3
import requests 
from JobsAddItem import addjob

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


def func_houzz(company, driver):
    driver.get('https://www.houzz.com/jobs?team=Engineering')
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "Santa Monica, CA, US")))
    except:
        print('didnt work')
        return company + 'didnt work'
    elem = driver.find_element_by_xpath("//a[@id='Santa Monica, CA, US']/../..")
    items = elem.find_elements_by_xpath("following-sibling::tr")
    for e in items:
        try:
            if e.get_attribute('class') != '': 
                break
            job_title = e.find_element_by_tag_name('span').text
            job_url = e.find_element_by_tag_name('a').get_attribute('href')
            # print(job_title)
            # print(job_url)
            print('')

            addjob(job_title, company, job_url)
        except:
            pass


def func_zillow(company, driver):
    driver.get('https://careers.zillowgroup.com/List-Jobs/type/Software-Development/location/Irvine,Los-Angeles,Riverside')
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "k-grid-content")))
    except:
        print('didnt work')
        return company + 'didnt work'
    elem = driver.find_element_by_class_name('k-grid-content')
    items = elem.find_elements_by_tag_name('tr')
    for e in items:
        try:
            job_title = e.find_element_by_tag_name('a').text
            job_url = e.find_element_by_tag_name('a').get_attribute('href')
            # print(job_title)
            # print(job_url)
            print('')

            addjob(job_title, company, job_url)
        except:
            pass


def func_kareo(company, driver):
    driver.get('https://kareoinc.applytojob.com/apply/jobs/')
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "jobs_table")))
    except:
        print('didnt work')
        return company + 'didnt work'
    elem = driver.find_element_by_id('jobs_table')
    items = elem.find_elements_by_tag_name('tr')
    for e in items:
        try:
            job_cat = e.find_element_by_class_name('resumator_department').text
            if job_cat.strip().lower() == 'development':
                job_title = e.find_element_by_tag_name('a').text
                job_url = e.find_element_by_tag_name('a').get_attribute('href')
                # print(job_title)
                # print(job_url)
                print('')

                addjob(job_title, company, job_url)
        except:
            pass


def func_ephesoft(company, driver):
    driver.get('https://ephesoft.com/careers/open-positions/')
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "bhrDepartmentID_18506")))
    except:
        print('didnt work')
        return company + 'didnt work'
    elem = driver.find_element_by_id('bhrDepartmentID_18506')
    elem2 = elem.find_element_by_class_name('BambooHR-ATS-Jobs-List')
    items = elem2.find_elements_by_tag_name('li')
    for e in items:
        try:
            job_title = e.find_element_by_tag_name('a').text
            job_url = e.find_element_by_tag_name('a').get_attribute('href')
            # print(job_title)
            # print(job_url)
            print('')
        
            addjob(job_title, company, job_url)
        except:
            pass
        

def func_ciedigital(company, driver):
    driver.get('https://www.ciedigital.com/careers/')
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "job-preview")))
    except:
        print('didnt work')
        return company + 'didnt work'
    
    elem = driver.find_elements_by_class_name('job-preview')
    for e in elem:
        try:
            job_cat = e.find_element_by_class_name('job-preview__category').text
            if job_cat.strip().lower() == 'engineering/it':
                job_title = e.find_element_by_class_name('job-preview__title').text
                job_url = e.find_element_by_class_name('job-preview__link').get_attribute('href')
                # print(job_cat)
                # print(job_title)
                # print(job_url)
                print('')

                addjob(job_title, company, job_url)
        except:
            pass
        

def func_acorns(company, driver):
    driver.get("https://www.acorns.com/careers/")
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "irvine")))
    except:
        print('didnt work')
        return company + 'didnt work'
    elem = driver.find_element_by_class_name('irvine')
    items = elem.find_elements_by_tag_name('li')

    for e in items:
        try:
            job_cat = e.find_element_by_tag_name('p').text
            if job_cat.strip() == 'Engineering':
                job_title = e.find_element_by_tag_name('strong').text
                job_url = e.find_element_by_tag_name('a').get_attribute('href')
                # print(job_cat)
                # print(job_title)
                # print(job_url)
                print('')
                
                addjob(job_title, company, job_url)
        except:
            pass
        
# AWS Lambda function
# Headless chrome browser to obtain scrape data from dynamic Websites
def my_function(event, context):
    print("Starting...")
    
    chrome_options = Options()

    #### Comment out when testing locally 
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    # Functions to target company's Website to scrape data
    # func_ciedigital('ciedigital', driver)
    # func_acorns('acorns', driver)
    # func_ephesoft('ephesoft', driver)
    # func_kareo('kareo', driver)
    # func_zillow('zillow', driver)
    func_houzz('houzz', driver)
    
    
    # Invoke Lambda for E-mail
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='my-function',
        InvocationType='RequestResponse'
    )            

    driver.close()
    return 'Successfully completed job.'


##### Comment out when running on AWS Lambda
# my_function('','')
