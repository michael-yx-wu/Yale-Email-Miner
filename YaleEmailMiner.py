#!/usr/bin/python2.7

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select, WebDriverWait
import os
import sys
import time

# Enter your netID password here
username, password = "xxxxxx", "xxxxxxx"

os.system("clear")
print "============= Yale Email Miner =============="

# Determine class years
senior      = int(raw_input("Year (YY) when the seniors graduate: "))
junior      = senior + 1
sophomore   = junior + 1
freshman    = sophomore + 1

# Determine which classes to mine
miningscope = str(raw_input("(1)Freshman (2)Sophomore (3)Junior (4)Senior\nWhich classes to mine: "))
mSenior = False
mJunior = False
mSophomore = False
mFreshman = False
if "1" in miningscope:
    mFreshman = True
if "2" in miningscope:
    mSophomore = True
if "3" in miningscope:
    mJunior = True
if "4" in miningscope:
    mSenior = True

# Start Chrome
sys.stdout.write("Current Page: ")
sys.stdout.flush()
driver = webdriver.Chrome()
driver.get("https://students.yale.edu/facebook")

# CAS Login
userfield = driver.find_element_by_xpath('//*[@id="username"]')
userfield.send_keys(username)
passfield = driver.find_element_by_xpath('//*[@id="password"]')
passfield.send_keys(password)
driver.find_element_by_xpath('//*[@id="form-layout"]/tbody/tr[5]/td[2]/input[3]').click()

# Set range to Yale College
select = Select(driver.find_element_by_xpath('//*[@id="college_title"]/form/select'))
select.select_by_value("Trumbull College")
select = Select(driver.find_element_by_xpath('//*[@id="college_title"]/form/select'))
select.select_by_value("Yale College")

# Different files for each class
berkeleyFile    = "Berkeley.txt"
branfordFile    = "Branford.txt"
calhounFile     = "Calhoun.txt"
davenportFile   = "Davenport.txt"

seniorFile      = "Yale%d.txt" %(senior)
juniorFile      = "Yale%d.txt" %(junior)
sophomoreFile   = "Yale%d.txt" %(sophomore)
freshmanFile    = "Yale%d.txt" %(freshman)
seniorFile      = open(seniorFile, 'w')
juniorFile      = open(juniorFile, 'w')
sophomoreFile   = open(sophomoreFile, 'w')
freshmanFile    = open(freshmanFile, 'w')
unsureFile      = open("YaleXX.txt", 'w')

# Other variables needed for fetching addresses
wait = ui.WebDriverWait(driver, 5)
currentpage = ""
totalEmails = 0
missingEmails = []
breakloop = False

# Sort emails and names into corresponding files
while True:
    # Wait for page load and print current page
    wait.until(lambda driver: driver.find_element_by_class_name("curr_link"))
    for i in range(len(currentpage)):
        sys.stdout.write('\b')
    currentpage = driver.find_element_by_class_name("curr_link").text
    sys.stdout.write(currentpage)
    sys.stdout.flush()

    # Get names and class and emails (9 per page)
    students = driver.find_elements_by_class_name("student_container")
        
    # Write name and emails to corresponding file
    for i in range(len(students)):
        # Find and parse name
        name = students[i].find_element_by_class_name("student_name").text
        nameToWrite = name[name.find(", ")+2:]+" "+name[:name.find(",")]

        # Look for student email, if missing, skip next steps
        try:
            email = students[i].find_element_by_class_name("email").text
            totalEmails += 1
        except:
            missingEmails.append(name)
            continue

        # Get student class and try to parse to int
        year = students[i].find_element_by_class_name("year_container").find_elements_by_tag_name("div")[0].text
        try:
            year = int(year[year.find("'")+1:])
        except:
            unsureFile.write((nameToWrite+","+email+'\n').encode('utf-8'))
            continue
        
        # Write to correct file
        if mSenior and year == senior:
            seniorFile.write((nameToWrite+","+email+'\n').encode('utf-8'))
        if mJunior and year == junior:
            juniorFile.write((nameToWrite+","+email+'\n').encode('utf-8'))
        if mSophomore and year == sophomore:
            sophomoreFile.write((nameToWrite+","+email+'\n').encode('utf-8'))
        if mFreshman and year == freshman:
            freshmanFile.write((nameToWrite+","+email+'\n').encode('utf-8'))

    # Break when no more pages (using try/catch just in case, the website is broken)
    try:
        # Next page of students
        if driver.find_element_by_xpath('//*[@id="content_container"]/div[2]/div[4]').get_attribute('class') == "next grey":
            breakloop = True
            break
        driver.find_element_by_xpath('//*[@id="content_container"]/div[2]/div[4]').click()
    except:
        breakloop = True
    if breakloop:
        break
    
print "\nTotal emails: %d" %(totalEmails)
seniorFile.close()
juniorFile.close()
sophomoreFile.close()
freshmanFile.close()
unsureFile.close()
for i in missingEmails:
    print "Missing email: %s" %(i)
driver.quit()
# os.remove("chromedriver.log")
