from app.scraping.ConcreteScrapers.LinkedInScraper import LinkedInScraper


class ScraperFactory:
    @staticmethod
    def get_scraper(site: str):
        scrapers = {"linkedin": LinkedInScraper()}

        return scrapers.get(site, None)
