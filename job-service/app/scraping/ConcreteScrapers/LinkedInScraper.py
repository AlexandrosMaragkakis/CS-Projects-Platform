import requests
from bs4 import BeautifulSoup
from ..BaseScraper import BaseScraper


class LinkedInScraper(BaseScraper):
    def __init__(self):
        pass

    def scrape(self, url):
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def extract_info(self, soup):
        title = (
            soup.find("h1", class_="top-card-layout__title").get_text(strip=True)
            if soup.find("h1", class_="top-card-layout__title")
            else "N/A"
        )
        company = (
            soup.find("a", class_="topcard__org-name-link").get_text(strip=True)
            if soup.find("a", class_="topcard__org-name-link")
            else "N/A"
        )
        description = (
            soup.find("div", class_="show-more-less-html__markup").get_text(
                " ", strip=True
            )
            if soup.find("div", class_="show-more-less-html__markup")
            else "N/A"
        )

        job_criteria = {}
        criteria_list = soup.find_all("li", class_="description__job-criteria-item")
        for item in criteria_list:
            header = item.find(
                "h3", class_="description__job-criteria-subheader"
            ).get_text(strip=True)
            value = item.find("span", class_="description__job-criteria-text").get_text(
                strip=True
            )
            job_criteria[header] = value

        return {
            "title": title,
            "company": company,
            "description": description,
            "seniority_level": job_criteria.get("Seniority level", "N/A"),
            "employment_type": job_criteria.get("Employment type", "N/A"),
            "job_function": job_criteria.get("Job function", "N/A"),
            "industries": job_criteria.get("Industries", "N/A"),
        }
