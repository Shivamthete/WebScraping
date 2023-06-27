import requests
import csv
import lxml
from bs4 import BeautifulSoup

file = open('linkedin-jobs.csv', 'a')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'Location', 'Apply'])

web_page = 'https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Canada&locationId=&geoId=101174742&f_TPR=r86400&position=1&pageNum=0&start='

page_number = 1

# A function to scrape all the pages, each page has 25 results

def linkedin_scraper(url, page_number):
   
    next_page = url + str(page_number)
    print(str(next_page))
    html_text = requests.get(str(next_page))
    soup = BeautifulSoup(html_text.content,'lxml')
    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for job in jobs:
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        job_location = job.find('span', class_='job-search-card__location').text.strip()
        job_link = job.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')['href']
        writer.writerow([job_title.encode('utf-8'), job_company.encode('utf-8'), job_location.encode('utf-8'), job_link.encode('utf-8')])

    print('Data updated')



    if page_number < 200:
        page_number = page_number + 25
        linkedin_scraper(url, page_number)
    else:
        file.close()
        print('File closed')

linkedin_scraper(web_page, page_number)


