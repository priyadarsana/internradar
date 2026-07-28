def internshala():
    # import libraries
    import os
    import pickle
    import requests
    from bs4 import BeautifulSoup

    company_name = "internshala"
    FILE_PATH = os.path.abspath(os.path.dirname(__file__))


    """
    PARSE AND SCRAPE WEBPAGES FOR CURRENT INTERNSHIP POSTINGS
    """
    # get and parse webpage
    # User-Agent is required — Internshala blocks default requests headers
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}
    url = "https://internshala.com/internships/computer-science-internship"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    job_listings = soup.find_all("div", class_="individual_internship")

    # loop through internship postings, store details in dict
    current_jobs_dict = {}

    for job_listing in job_listings:
        try:
            # title and link
            title_tag = job_listing.find("a", class_="job-title-href")
            title = title_tag.get_text(strip=True)
            rel_link = title_tag["href"]
            link = f"https://internshala.com{rel_link}"

            # company name
            company_tag = job_listing.find("p", class_="company-name")
            company = company_tag.get_text(strip=True) if company_tag else "N/A"

            # location — one or more <a> tags inside .locations span
            locations_div = job_listing.find("div", class_="locations")
            if locations_div:
                location_tags = locations_div.find_all("a")
                location = ", ".join(t.get_text(strip=True) for t in location_tags) or "N/A"
            else:
                location = "N/A"

            # stipend — <span class="stipend">
            stipend_tag = job_listing.find("span", class_="stipend")
            stipend = stipend_tag.get_text(strip=True) if stipend_tag else "N/A"

            # posting date — relative label in detail-row-2 (e.g. "Just now", "2 days ago")
            row2 = job_listing.find("div", class_="detail-row-2")
            if row2:
                status_div = row2.find("div", class_="status-success")
                date_posted = status_div.find("span").get_text(strip=True) if status_div else "N/A"
            else:
                date_posted = "N/A"

            current_jobs_dict[link] = {
                "title": title,
                "company": company,
                "location": location,
                "date_posted": date_posted,
                "link": link,
                "details": stipend,
            }

        except Exception:
            # skip broken listings without crashing the whole scrape
            continue


    """
    LOAD RESULTS OF LAST EXECUTION - STORE CURRENT RESULTS
    """
    # open last saved internship postings (create empty dict if nonexistent)
    try:
        with open(f'{FILE_PATH}/{company_name}_current_jobs_dict.pkl', 'rb') as f:
            saved_jobs_dict = pickle.load(f)
    except FileNotFoundError:
        saved_jobs_dict = {}

    # store current state of internship postings for next execution
    with open(f'{FILE_PATH}/{company_name}_current_jobs_dict.pkl', 'wb') as f:
        pickle.dump(current_jobs_dict, f)


    """
    FILTER JOBS AND RETURN RESULTS AS DICTIONARY
    """
    # create dict containing only new internships (not seen in last run)
    new_jobs = {job: current_jobs_dict[job] for job in current_jobs_dict if job not in saved_jobs_dict}
    # create written summary
    summary = f"{len(job_listings)} listings found, {len(current_jobs_dict)} scraped, {len(new_jobs)} new jobs."

    return (summary, new_jobs)
