import re
import pytest
from playwright.sync_api import expect
from config import REPO_UI_URL
from helpers import log_step
from helpers import parse_star_count



@pytest.mark.parametrize("repo_data", [
    {"name": "vscode", "owner": "microsoft", "stars": ">100k", "readme_visible": True}
])
def test_repo_page_loads(page, repo_data):
    log_step(f"Loading {repo_data['name']} repo, hmmm?")
    page.goto(REPO_UI_URL)
    
    expect(page.get_by_role("heading", name=repo_data["name"])).to_be_visible()
    log_step("Repository name verified!")
    
    expect(page.locator("span[itemprop='author']")).to_contain_text(repo_data["owner"])
    log_step("Owner confirmed, microsoft it is.")
    
    star_text = page.locator("#repo-stars-counter-star").inner_text()
    stars = parse_star_count(star_text)
    assert stars > 100000, f"Expected {repo_data['stars']} stars, got {stars}"
    log_step(f"Star count {stars} > 100k, popular this repo is.")


    expect(page.locator("#repo-network-counter")).to_be_visible()
    log_step("Fork count visible, many forks there are.")

    expect(page.locator('span[data-content="README"]')).to_be_visible()
    log_step("README rendered, markdown magic works.")


def test_code_navigation_and_typescript_file(page):
    page.goto(REPO_UI_URL)

    log_step("Navigating to src folder")
    # Yeh commit links ko filter out kar dega
    page.get_by_role("link", name="src, (Directory)").first.click()    
    page.wait_for_url("**/src")
    log_step("URL changed to show content inside src folder")

    breadcrumb_src = page.get_by_role("heading", name="src")
    expect(breadcrumb_src).to_be_visible()

    log_step("Opening a TypeScript file")

    ts_href = page.locator("a[aria-label$='.ts, (File)']").first.get_attribute("href")
    assert ts_href is not None
    page.goto(f"https://github.com{ts_href}")
    log_step("Opened TS File")

    code = page.locator("div.react-code-lines >> div.react-code-text").first
    expect(code).to_be_visible()
    line_numbers = page.locator("div.react-line-number")
    expect(line_numbers.first).to_be_visible()
    assert line_numbers.count() > 0

def test_repo_stats_and_metadata(page):
    page.goto(REPO_UI_URL)

    about_section = page.locator("div.BorderGrid.about-margin")
    expect(about_section).to_be_visible()

    description = about_section.locator("p").filter(has_text=re.compile(".+")).first

    expect(description).to_be_visible()
    assert description.inner_text().strip() != ""
    log_step(description.inner_text().strip())

    license_link = about_section.locator("a").filter(has_text="license")

    assert license_link.count() > 0, "License Information not found"

    topics = page.locator("a.topic-tag")
    assert topics.count() > 0, "Topics/tags not found"







