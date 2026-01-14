import pytest
from playwright.sync_api import expect
from config import REPO_UI_URL
from conftest import logger 
from helpers import parse_star_count



@pytest.mark.parametrize("repo_data", [
    {"name": "vscode", "owner": "microsoft", "stars": ">100k", "readme_visible": True}
])
def test_repo_page_loads(page, repo_data):
    logger.info(f"Loading {repo_data['name']} repo, hmmm?")
    page.goto(REPO_UI_URL)
    
    expect(page.get_by_role("heading", name=repo_data["name"])).to_be_visible()
    logger.info("Repository name verified!")
    
    expect(page.locator("span[itemprop='author']")).to_contain_text(repo_data["owner"])
    logger.info("Owner confirmed, microsoft it is.")
    
    star_text = page.locator("#repo-stars-counter-star").inner_text()
    stars = parse_star_count(star_text)
    assert stars > 100000, f"Expected >100k stars, got {stars}"
    logger.info(f"Star count {stars} > 100k, popular this repo is.")


    expect(page.locator("#repo-network-counter")).to_be_visible()
    logger.info("Fork count visible, many forks there are.")

    expect(page.locator('span[data-content="README"]')).to_be_visible()
    logger.info("README rendered, markdown magic works.")