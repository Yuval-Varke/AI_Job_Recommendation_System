from apify_client import ApifyClient
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Fetch LinkedIn jobs based on search query and location
def fetch_linkedin_jobs(search_query, location="india", rows=60):
    search_url = (
        "https://www.linkedin.com/jobs/search/?keywords="
        f"{quote_plus(search_query)}&location={quote_plus(location)}"
    )
    run_input = {
        "urls": [search_url],
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }
    run = apify_client.actor("hKByXkMQaC5Qt9UMN").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


# Fetch Naukri jobs based on search query and location
def fetch_naukri_jobs(search_query, location = "india", rows=60):
    run_input = {
        "keyword": search_query,
        "maxJobs": 60,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }
    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs