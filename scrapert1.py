from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

#Initializing the webdriver
coptions = webdriver.ChromeOptions()

#Uncomment the line below if you'd like to scrape without a new Chrome window every time.
#options.add_argument('headless')

#Change the path to where chromedriver is in your home folder.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = coptions)
driver.set_window_size(1120, 1000)

url = 'https://www.glassdoor.com/Job/united-arab-emirates-software-engineer-jobs-SRCH_IL.0,20_IN6_KO21,38.htm?context=Jobs&clickSource=searchBox'
driver.get(url)
page_number = 1

# Initialize a list to store the job details
job_data = []

while page_number <= 2:
    
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

    # Scrape job title for each listing
    for job in job_listings:
        try:
            job_title_element = job.find_element(By.XPATH, ".//div[@class='job-title mt-xsm']")
            job_title = job_title_element.text
            if job_title_element:
                job_title = job_title_element.text
                print("Job Title:", job_title)

            employer_element = job.find_element(By.XPATH, ".//div[@class='job-search-8wag7x']")
            employer = employer_element.text
            if employer_element:
                employer = employer_element.text
                print("Employer:", employer)
            else:
                employer = -1


            salary_element = job.find_element(By.XPATH, ".//div[@class='salary-estimate']")
            salary = salary_element.text
            if salary_element:
                salary = salary_element.text
                print("Estimated Salary:", salary)
            else:
                salary_element = -1
            
            location_element = job.find_element(By.XPATH, ".//div[@class='location mt-xxsm']")
            location = location_element.text
            if location_element:
                location = location_element.text
                print("Location:", location)
            else:
                location_element = -1

            # Append job details to the list
            job_data.append({"Job Title": job_title, "Employer": employer, "Estimated Salary": salary, "Location": location})

        except NoSuchElementException:
            print("Failed to scrape job details for a listing.")
        
    # Check if there is a next page
    next_button = driver.find_element(By.XPATH, "//button[@class='nextButton job-search-opoz2d e13qs2072']")
    if "disabled" in next_button.get_attribute("class"):
        # No more pages to load, break the loop
        break
    else:
        # Click on the next page button to load the next set of job listings
        next_button.click()
        time.sleep(2)  # Add a small delay to allow the page to load
    
    page_number += 1
        

# Close the webdriver
driver.quit()

# Convert the job data list into a DataFrame
df = pd.DataFrame(job_data)

# Save the DataFrame to a CSV file
df.to_csv("job_details.csv", index=False)