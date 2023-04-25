from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_page_count(keyword):
    options = Options()
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    browser = webdriver.Chrome(options=options)

    base_url = "https://ca.indeed.com/jobs?q="
    browser.get(f"{base_url}{keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", class_ = "ecydgvn0")
    pages = pagination.find_all("div", class_ = "ecydgvn1")

    if not pages:
        return 1
    count = len(pages)
    
    if count >= 5:
        return 5
    else:
        return count

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    
    # empty list for jobs description
    results = []
    
    for page in range(pages):        
        options = Options()
        browser = webdriver.Chrome(options=options)

        # opening the website using selenium
        base_url = "https://ca.indeed.com/jobs"
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        print("Requesting", final_url)
        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_ = "jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find("div", class_ = "mosaic-zone")
            if zone == None:
                h2 = job.find("h2", class_ = "jobTitle")
                anchor = job.select_one("h2 a")
                if anchor != None:
                    title = anchor['aria-label']
                    link = anchor['href']
                    company = job.find("span", class_ = "companyName")
                    location = job.find("div", class_ = "companyLocation")
                    job_data = {
                        'link': f"https://ca.indeed.com{link}",
                        'company': company.string,
                        'location': location.string,
                        'position': title
                    }
                    for each in job_data:
                        if job_data[each] != None:
                            job_data[each] = job_data[each].replace(",", " ")
                    results.append(job_data)
        return results
    
