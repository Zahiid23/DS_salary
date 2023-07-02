from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


def scrape_jobs(keyword):
    #Initializing the webdriver
    coptions = webdriver.ChromeOptions()

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')

    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = coptions)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/united-arab-emirates-'+keyword+'-jobs-SRCH_IL.0,20_IN6_KO21,38.htm?context=Jobs&clickSource=searchBox'
    driver.get(url)
    page_number = 1

    # Initialize a list to store the job details
    job_data = []

    while page_number < 31:
        
        # Close the signup prompt if it appears
        try:
            close_button = driver.find_element(By.XPATH, "//button[@class='e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40']")
            close_button.click()
            print("Closed the signup prompt")
        except NoSuchElementException:
            print("Signup prompt not found, continue with scraping")
            pass
            

        # Find job listings on the page
        job_listings = driver.find_elements(By.XPATH, ".//li[contains(@class, 'react-job-listing')]")

        actions = ActionChains(driver)

        # Scrape job for each listing
        for job in job_listings:
            try:
                job_title_element = job.find_element(By.XPATH, ".//div[@class='job-title mt-xsm']")
                job_title = job_title_element.text
                if job_title_element:
                    job_title = job_title_element.text
                    print("Job Title:", job_title)
            except NoSuchElementException:
                job_title = "NA"

            try:
                employer_element = job.find_element(By.XPATH, ".//div[@class='job-search-8wag7x']")
                employer = employer_element.text
                if employer_element:
                    employer = employer_element.text
                    print("Employer:", employer)
            except NoSuchElementException:
                employer = "NA"

            try:
                salary_element = job.find_element(By.XPATH, ".//div[@class='salary-estimate']")
                salary = salary_element.text
                if salary_element:
                    salary = salary_element.text
                    print("Estimated Salary:", salary)
            except NoSuchElementException:
                salary = "NA"
            
            try:
                location_element = job.find_element(By.XPATH, ".//div[@class='location mt-xxsm']")
                location = location_element.text
                if location_element:
                    location = location_element.text
                    print("Location:", location)
            except NoSuchElementException:
                location = "NA"

            # Append job details to the list
            job_data.append({"Job Title": job_title, "Employer": employer, "Estimated Salary": salary, "Location": location})
            
            actions.move_to_element(job)
            actions.perform()
    
        # Check if there is a next page
        next_button = driver.find_element(By.XPATH, "//button[@class='nextButton job-search-opoz2d e13qs2072']")
        if "disabled" in next_button.get_attribute("class"):
            # No more pages to load, break the loop
            break
        else:
            # Click on the next page button to load the next set of job listings
            next_button.click()
            time.sleep(5)  # Add a small delay to allow the page to load
        
        page_number += 1
            

    # Close the webdriver
    driver.quit()

    # Convert the job data list into a DataFrame
    return pd.DataFrame(job_data)

df = scrape_jobs('software')

df.to_csv("scraped_jobs.csv", index=False)

