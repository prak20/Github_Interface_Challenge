# import pytest
# from playwright.sync_api import Page, expect
# from loguru import logger
# # from config import REPO_UI_URL
# from helpers import parse_star_count

# REPO_UI_URL = "https://github.com/microsoft/vscode"


# @pytest.mark.ui
# def test_repo_page_loads(page: Page):
#     """Repository page loads hmmm, displays correctly it does"""
#     logger.info("Starting repo page load test")
#     page.goto(REPO_UI_URL)
    
#     expect(page).to_have_title("GitHub - microsoft/vscode: Visual Studio Code")
#     # owner_locator = page.locator("a[href='https://github.com/microsoft']")
#     # repo_name_locator = page.locator("strong[itemprop='name'] a")

#     # expect(owner_locator).to_be_visible()
#     # expect(repo_name_locator).to_have_text("vscode")


#     # expect(page.locator("h1 strong").filter(has_text="microsoft/vscode")).to_be_visible()
#     # expect(page.get_by_text("microsoft")).to_be_visible()

#     expect(page.locator("h1 strong").filter(has_text="microsoft/vscode")).to_be_visible()
#     expect(page.get_by_text("microsoft")).to_be_visible()
    
#     star_locator = page.locator('[data-testid="repo-star-count"]').first
#     expect(star_locator).to_be_visible()
#     logger.info(f"Stars visible: {star_locator.text_content()}")

#     star_text = star_locator.first.inner_text()
#     stars = parse_star_count(star_text)
#     assert stars > 100_000, f"Expected >100k stars, got {stars}"
    
#     forks_locator = page.locator('[data-testid="repo-fork-count"]').first
#     expect(forks_locator).to_be_visible()
#     logger.info(f"Forks visible: {forks_locator.text_content()}")
    
#     # README rendered
#     expect(page.locator("[data-testid='readme-container']").first).to_be_visible()
#     logger.info("Repo page loaded successfully")




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