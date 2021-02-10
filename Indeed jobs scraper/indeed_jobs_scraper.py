import requests, sqlite3
from bs4 import BeautifulSoup

# get the pages content with requests library
def  extract(keyword, page):
    result = requests.get('https://www.indeed.com/jobs?q={keyword}&start={page}')
    soup = BeautifulSoup(result.content, 'lxml')
    return soup


# scrap the data we need and insert them into dict
def transform(soup):
    divs = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})
    for item in divs:
        title = item.a.text.strip()
        company = item.find('span', class_='company').text.strip()
        summary = item.find('div', class_='summary').text.strip()
        try:
            salary = item.find('span', class_='salaryText').text.strip()
        except: salary = 'none'
        # print('#' * 20, summary, end='\n \n \n')
        job = {
            'title': title,
            'company': company,
            'summary': summary,
            'salary': salary
        }
        job_list.append(job)
        

# Create DB and delete the past data

db = sqlite3.connect('jobs.db')
cr = db.cursor()
cr.execute(
    'create table if not exists jobs (title text, company text, summary text, salary text, job_id integer)'
)

cr.execute('DELETE from jobs')

# Create list to insert jobs into it
job_list = []

# Loop on multiple pages
for  page in range(0, 30, 10):
    
    # Loop on jobs on one page
    for i in range(15):      
        c = extract('python', page)
        transform(c)

        title = job_list[i]['title']
        company = job_list[i]['company']
        summary = job_list[i]['summary']
        salary = job_list[i]['salary']
        
        print(title)
        cr.execute(
            f'INSERT INTO jobs(title, company, salary, summary, job_id) values("{title}", "{company}", "{salary}", "{summary}", {i})')




# Close DB
db.commit()
db.close()
