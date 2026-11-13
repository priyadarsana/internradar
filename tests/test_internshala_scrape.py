import requests

from websites.internshala import internshala_scrape


class FakeResponse:
    text = """
    <div class="individual_internship">
      <a class="job-title-href" href="/internship/detail-analyst">Data Analyst</a>
      <p class="company-name">Example Labs</p>
      <div class="locations"><a>Berlin</a><a>Remote</a></div>
      <span class="stipend">€500 / month</span>
      <div class="detail-row-2"><div class="status-success"><span>2 days ago</span></div></div>
    </div>
    """


def test_internshala_parses_listing_and_reports_it_only_once(monkeypatch, tmp_path):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: FakeResponse())
    monkeypatch.setattr(internshala_scrape, "__file__", str(tmp_path / "internshala_scrape.py"))

    summary, new_jobs = internshala_scrape.internshala()

    assert summary == "1 listings found, 1 scraped, 1 new jobs."
    assert new_jobs == {
        "https://internshala.com/internship/detail-analyst": {
            "title": "Data Analyst",
            "company": "Example Labs",
            "location": "Berlin, Remote",
            "date_posted": "2 days ago",
            "link": "https://internshala.com/internship/detail-analyst",
            "details": "€500 / month",
        }
    }

    second_summary, second_new_jobs = internshala_scrape.internshala()

    assert second_summary == "1 listings found, 1 scraped, 0 new jobs."
    assert second_new_jobs == {}