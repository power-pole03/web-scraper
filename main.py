from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs

keyword = input("What do you want to search for?")

wwr = extract_wwr_jobs(keyword)
indeed = extract_indeed_jobs(keyword)

jobs = wwr + indeed

for job in jobs:
    print(job)
    print("/////\n/////")