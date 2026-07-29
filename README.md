# InternRadar

Automated job and internship scraper that monitors multiple career sites, detects only new postings, and sends email alerts when matches appear.

## Overview

Searching job boards by hand is repetitive and easy to miss. InternRadar automates that workflow by checking several sources on a schedule, comparing each scrape against cached results, and notifying you only when something new is found.

## Features

- Scrapes 7 sources: Ipsos, NiQ, index_de, Ottobock, RECUP, The Female Company, and Internshala.
- Uses `Requests` and `BeautifulSoup` for HTML scraping.
- Saves scrape results as pickle cache files inside each site folder under `websites/`.
- Compares each run against the previous cache to detect only new postings.
- Sends Gmail SMTP email alerts only when new jobs or internships are found.
- Includes job title, company, link, location, and extra details such as stipend where available.
- Runs fully automated every 6 hours through GitHub Actions.
- Commits updated cache files back to the repository so state persists between runs.

## Tech Stack

- Python
- Requests
- BeautifulSoup
- GitHub Actions
- SMTP via Gmail

## Architecture

Each scraper collects the latest postings from one source and stores the results in a pickle cache. On the next run, InternRadar compares the fresh scrape with the saved cache, keeps only the new entries, and builds an email alert from those results. The full flow is automated by a GitHub Actions cron job, so no server is required.

## Setup

```bash
git clone <your-repo-url>
cd internradar
python -m venv .venv
.venv\Scripts\activate
pip install python-dotenv requests beautifulsoup4 selenium
```

Create a `.env` file in the project root:

```env
EMAIL_ADDRESS=your_gmail_address@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_TO=destination_email@example.com
```

Run the scraper locally:

```bash
python job_scrape.py
```

## Automation

InternRadar is designed to run unattended through GitHub Actions every 6 hours. Add the email credentials as repository secrets, and the workflow will:

- check out the repository,
- install the Python dependencies,
- run `python job_scrape.py`,
- commit any updated pickle cache files back to the repo.

This keeps the deduplication state persistent without needing a database or server.

## Future Improvements

- Add a dashboard for visualizing posting trends over time.
- Expand coverage with more job and internship sources.

## Credits

This project started by studying an open-source job scraper pattern and was then substantially extended with new sources, custom deduplication, an Internshala scraper built from scratch, and the GitHub Actions automation layer.
