from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By


def get_jobs(keyword, num_jobs, verbose):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1120, 1000)
    
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    job_buttons_list = []
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(1)

        try:
            driver.find_element(By.XPATH, '/html/body/div[11]/div[2]/div[2]/div[1]/div[1]/button').click() #clicking to the X.
        except NoSuchElementException:
            pass
        
        #Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__wjTHv")

        count = 1
        for job_button in job_buttons:

            if job_button not in job_buttons_list:

                print(count, "\n")

                print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
                if len(jobs) >= num_jobs:
                    break

                try:
                    driver.find_element(By.XPATH,
                                        '/html/body/div[11]/div[2]/div[2]/div[1]/div[1]/button').click()  # clicking to the X.
                except NoSuchElementException:
                    pass

                try:
                    job_button.click()  #You might
                except ElementNotInteractableException:
                    break

                job_buttons_list.append(job_button)

                time.sleep(1)
                collected_successfully = False

                try:
                    driver.find_element(By.XPATH,
                                        '/html/body/div[11]/div[2]/div[2]/div[1]/div[1]/button').click()  # clicking to the X.
                except NoSuchElementException:
                    pass

                while not collected_successfully:
                    try:
                        try:
                            company_name = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/header/div[1]/a/div[2]/h4').text
                        except NoSuchElementException:
                            company_name = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[10]/div/div/div[1]/div[1]/div[1]').text
                        location = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/header/div[1]/div').text
                        job_title = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/header/div[1]/h1').text
                        job_description = driver.find_element(By.CLASS_NAME, 'JobDetails_jobDescription__uW_fK').text
                        collected_successfully = True
                    except:
                        time.sleep(1)

                try:
                    driver.find_element(By.XPATH,
                                        '/html/body/div[11]/div[2]/div[2]/div[1]/div[1]/button').click()  # clicking to the X.
                except NoSuchElementException:
                    pass

                try:
                    salary_estimate = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/div[1]/section/section[1]/div/div[1]/div[2]/div[1]').text
                except NoSuchElementException:
                    salary_estimate = -1 #You need to set a "not found value. It's important."

                try:
                    rating = driver.find_element(By.XPATH, '//*[@id="rating-headline"]').text
                except NoSuchElementException:
                    rating = -1 #You need to set a "not found value. It's important."

                try:
                    driver.find_element(By.XPATH,
                                        '/html/body/div[11]/div[2]/div[2]/div[1]/div[1]/button').click()  # clicking to the X.
                except NoSuchElementException:
                    pass

                #Printing for debugging
                if verbose:
                    print("Job Title: {}".format(job_title))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))

                try:
                    driver.find_element(By.XPATH,
                                        '/html/body/div[11]/div[2]/div[2]/div[1]/div[1]/button').click()  # clicking to the X.
                except NoSuchElementException:
                    pass

                #Going to the Company tab...
                #clicking on this:
                #<div class="tab" data-tab-type="overview"><span>Company</span></div>
                try:
                    driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]').click()

                    try:
                        size = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[1]/div').text
                    except NoSuchElementException:
                        size = -1

                    try:
                        founded = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[2]/div').text
                    except NoSuchElementException:
                        founded = -1

                    try:
                        type_of_ownership = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[3]/div').text
                    except NoSuchElementException:
                        type_of_ownership = -1

                    try:
                        industry = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[4]/div').text
                    except NoSuchElementException:
                        industry = -1

                    try:
                        sector = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[5]/div').text
                    except NoSuchElementException:
                        sector = -1

                    try:
                        revenue = driver.find_element(By.XPATH, '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div/div[1]/section/section[2]/div/div/div[6]/div').text
                    except NoSuchElementException:
                        revenue = -1

                except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1

                try:
                    driver.find_element(By.XPATH,
                                        '/html/body/div[11]/div[2]/div[2]/div[1]/div[1]/button').click()  # clicking to the X.
                except NoSuchElementException:
                    pass

                if verbose:
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type of Ownership: {}".format(type_of_ownership))
                    print("Industry: {}".format(industry))
                    print("Sector: {}".format(sector))
                    print("Revenue: {}".format(revenue))
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

                jobs.append({"Job Title" : job_title,
                "Salary Estimate" : salary_estimate,
                "Job Description" : job_description,
                "Rating" : rating,
                "Company Name" : company_name,
                "Location" : location,
                "Size" : size,
                "Founded" : founded,
                "Type of ownership" : type_of_ownership,
                "Industry" : industry,
                "Sector" : sector,
                "Revenue" : revenue})
                #add job to jobs

                count+=1

        #Clicking on the "Show More" button
        try:
            driver.find_element(By.XPATH,
                                '/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/div/button').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.