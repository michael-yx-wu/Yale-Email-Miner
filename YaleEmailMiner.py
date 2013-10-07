#!/usr/local/bin/python
import keyring
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select, WebDriverWait
import os
import sys
import time

# Enter your netID password here
username = "myw5"
password = keyring.get_password("Yale CAS Login", username)

os.system("clear")
print "============= Yale Email Miner =============="

# Determine class years
senior      = int(raw_input("Year (YY) when the seniors graduate: "))
junior      = senior + 1
sophomore   = junior + 1
freshman    = sophomore + 1

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
seniorFile      = open("Yale%d.txt" %(senior), 'w')
juniorFile      = open("Yale%d.txt" %(junior), 'w')
sophomoreFile   = open("Yale%d.txt" %(sophomore), 'w')
freshmanFile    = open("Yale%d.txt" %(freshman), 'w')
unsureFile      = open("YaleClassUnknown.txt", 'w')
college1        = open("Berkeley.txt", 'w')
college2        = open("Branford.txt", 'w')
college3        = open("Calhoun.txt", 'w')
college4        = open("Davenport.txt", 'w')
college5        = open("EzraStiles.txt", 'w')
college6        = open("JonathanEdwards.txt", 'w')
college7        = open("Morse.txt", 'w')
college8        = open("Pierson.txt", 'w')
college9        = open("Saybrook.txt", 'w')
college10       = open("Silliman.txt", 'w')
college11       = open("TimothyDwight.txt", 'w')
college12       = open("Trumbull.txt", 'w')

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
        
        # Sort by class year
        if year == senior:
            seniorFile.write((nameToWrite+","+email+'\n').encode('utf-8'))
        if year == junior:
            juniorFile.write((nameToWrite+","+email+'\n').encode('utf-8'))
        if year == sophomore:
            sophomoreFile.write((nameToWrite+","+email+'\n').encode('utf-8'))
        if year == freshman:
            freshmanFile.write((nameToWrite+","+email+'\n').encode('utf-8'))

        # Sort by college

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
