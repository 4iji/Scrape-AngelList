# -*- coding: utf-8 -*-
"""
AngelList.com Web Scraping: Scrape AngelList.com Companies results and export attributes to CSV.
Example Link: https://angel.co/companies?locations[]=New+York&company_types[]=Startup

Instructions: Scroll down to the bottom and follow steps 1, 2, and 3.
This script requires that Firefox is installed. Recent versions of
Firefox may not work with the Selenium package utilized in Step 1. 
Please use Firefox 46 or earlier.

Created on Sat Aug 06 2016
@author: DWolf
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import unicodecsv as csv

# Function for opening the WebDriver, logging in, and scrolling
def FFwebdriver(email, password):
    driver = webdriver.Firefox()
    # Log in
    driver.get('https://angel.co/login?utm_source=top_nav_job_listings_browse')
    element = driver.find_element_by_id("user_email")
    element.send_keys(email)
    element = driver.find_element_by_id("user_password")
    element.send_keys(password)
    driver.find_element_by_name("commit").click()
    
    # Navigate to the right page for scraping
    driver.get('https://angel.co/companies?locations[]=New+York&company_types[]=Startup')
    
    pause = 3
    # Advanced Optional tip: Sort different ways to circumvent the 20-page/400-company limit    
    #time.sleep(pause)
    #driver.find_element_by_css_selector(".column.joined.sortable").click()
    #for i in range(1,5):
    #    print i
    #    driver.find_element_by_class_name('fontello-right-dir').click()
    #time.sleep(pause)
    #driver.find_element_by_css_selector(".column.raised.sortable").click()
    #driver.find_element_by_css_selector(".column.hiring_salary.sortable").click()
    #driver.find_element_by_css_selector(".column.hiring_equity.sortable").click()
    
    # Automatically scroll until you reach the 20-page/400 company limit
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        driver.find_element_by_class_name('more').click()
        time.sleep(pause)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
        
    time.sleep(pause)
    htmlResults = driver.page_source
    driver.quit()
    print("Step 1-Done")
    return htmlResults

# Function for parsing and scraping the HTML for the key attributes
def scraping(html):
    soup = BeautifulSoup(html, 'html.parser')
    raw_companies = soup.find_all('div', class_='base startup')
    #print len(raw_companies)
    #for target in raw_companies:
    #    print target.__str__()
    #    print "NEXT"
    company_list = list()
    
    #Iterate and pull out the key attributes
    for targetsoup in raw_companies:
        # Company Name---------------------------------------------------------
        # Need to find the SECOND class="startup-link" for the Company Name
        company_name = targetsoup.find_all("a", class_="startup-link")[1].get_text().strip('\n')
        #print(company_name)
        try: # AngelList Link--------------------------------------------------
            angellist_website = targetsoup.find("a", class_="startup-link").get('href').strip('\n')
            #print(angellist_website)
        except AttributeError:
            angellist_website = "Empty section for this company"
        try: # Company Tagline-------------------------------------------------
            tagline = targetsoup.find("div", class_="pitch").get_text().strip('\n')
            #print(tagline)
        except AttributeError:
            tagline = "Empty section for this company"
        try: # Signal----------------------------------------------------------
            # The class name can change depending on if it is visible or selected...
            signal = targetsoup.find("div", class_="column selected signal").findChild("img").get('alt').strip('\n')
            #signal = targetsoup.find("div", class_="column signal").findChild("img").get('alt').strip('\n')
            #signal = targetsoup.find("div", class_="column hidden_column signal").findChild("img").get('alt').strip('\n')
            #print(signal)
        except AttributeError:
            signal = "Empty section for this company"
        try: # Joined----------------------------------------------------------
            joined = targetsoup.find("div", class_="column joined selected").findChild("div", class_="value").get_text().strip('\n')
            #joined = targetsoup.find("div", class_="column hidden_column joined").findChild("div", class_="value").get_text().strip('\n')
            #print(joined)
        except AttributeError:
            joined = "Empty section for this company"
        try: # Location--------------------------------------------------------
            location = targetsoup.find("div", class_="column location").findChild("a").get_text().strip('\n')
            #location = targetsoup.find("div", class_="column hidden_column location").findChild("a").get_text().strip('\n')
            #print(location)
        except AttributeError:
            location = "Empty section for this company"
        try: # Market----------------------------------------------------------
            market = targetsoup.find("div", class_="column market").findChild("a").get_text().strip('\n')
            #market = targetsoup.find("div", class_="column hidden_column market").findChild("a").get_text().strip('\n')
            #print(market)
        except AttributeError:
            market = "Empty section for this company"
        try: # Website---------------------------------------------------------
            website = targetsoup.find("div", class_="column website").findChild("a").get('href').strip('\n')
            #print(website)
        except AttributeError:
            website = "Empty section for this company"
        try: # Employees-------------------------------------------------------
            employees = targetsoup.find("div", class_="column company_size").findChild("div", class_="value").get_text().strip('\n')
            #print(employees)
        except AttributeError:
            employees = "Empty section for this company"
        try: # Stage-----------------------------------------------------------
            stage = targetsoup.find("div", class_="column stage").findChild("div", class_="value").get_text().strip('\n')
            #print(stage)
        except AttributeError:
            stage = "Empty section for this company"
        try: # Total Raised----------------------------------------------------
            raised = targetsoup.find("div", class_="column hidden_column raised").findChild("div", class_="value").get_text().strip('\n')
            #raised = targetsoup.find("div", class_="column raised").findChild("div", class_="value").get_text().strip('\n')
            #print(raised)
        except AttributeError:
            raised = "Empty section for this company"
        try: # Job Positions---------------------------------------------------
            positions = targetsoup.find("div", class_="column hidden_column hiring_positions").findChild("div", class_="value").get_text().strip('\n')
            #positions = targetsoup.find("div", class_="column hiring_positions").findChild("div", class_="value").get_text().strip('\n')
            #print(positions)
        except AttributeError:
            positions = "Empty section for this company"
        try: # Salary----------------------------------------------------------
            salary = targetsoup.find("div", class_="column hidden_column hiring_salary").findChild("div", class_="value").get_text().strip('\n')
            #salary = targetsoup.find("div", class_="column hiring_salary").findChild("div", class_="value").get_text().strip('\n')
            #print(salary)
        except AttributeError:
            salary = "Empty section for this company"
        try: # Equity----------------------------------------------------------
            equity = targetsoup.find("div", class_="column hidden_column hiring_equity").findChild("div", class_="value").get_text().strip('\n')
            #equity = targetsoup.find("div", class_="column hiring_equity selected").findChild("div", class_="value").get_text().strip('\n')
            #print(equity)
        except AttributeError:
            equity = "Empty section for this company"

        company_dict = {'name': company_name, 
                    'AngelList_website': angellist_website,
                    'tagline': tagline, 
                    'signal': signal, 
                    'joined': joined,
                    'location': location, 
                    'market': market,
                    'website': website, 
                    'employees': employees, 
                    'stage': stage, 
                    'total_raised': raised, 
                    'job_positions': positions, 
                    'salary': salary, 
                    'equity': equity}
        company_list.append(company_dict)
    
    #print(company_list)
    print("Step 2-Done")
    return company_list

# Function for exporting the results to CSV
def exportingToCSV(company_list):
    
    with open('angelist-companies.csv','w') as outfile:
        writer = csv.DictWriter(outfile, company_list[0].keys())
        writer.writeheader()
        writer.writerows(company_list)
        
    print("Step 3-Done")



# Step 1: Firefox WebDriver
# This step will log in, navigate, and scroll to the appropriate webpage view
# Please enter AngelList account email and password
email = 'example@domain.com'
password = 'password'
html = FFwebdriver(email, password)

# Step 2: Web scraping
# This step will parse the HTML and identify the key columns
companies = scraping(html)

# Step 3: Export to CSV
exportingToCSV(companies)
