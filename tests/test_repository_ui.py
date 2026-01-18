import re
import pytest
from playwright.sync_api import expect
from config import REPO_UI_URL
from helpers import log_step
from helpers import parse_star_count

@pytest.mark.ui
@pytest.mark.parametrize("repo_data", [
    {"name": "vscode", "owner": "microsoft", "stars": ">100k", "readme_visible": True}
])
def test_repo_page_loads(page, repo_data):
    """Verify repository page loads with correct metadata."""
    log_step(f"Loading {repo_data['name']} repository")
    page.goto(REPO_UI_URL)
    log_step(f"Page loaded: {REPO_UI_URL}")
    
    expect(page.get_by_role("heading", name=repo_data["name"])).to_be_visible()
    log_step(f"Repository name '{repo_data['name']}' is visible")
    
    expect(page.locator("span[itemprop='author']")).to_contain_text(repo_data["owner"])
    log_step(f"Owner '{repo_data['owner']}' verified")
    
    star_text = page.locator("#repo-stars-counter-star").inner_text()
    stars = parse_star_count(star_text)
    assert stars > 100000, f"Expected {repo_data['stars']} stars, got {stars}"
    log_step(f"Stars: {stars:,} (validated > 100k)")


    expect(page.locator("#repo-network-counter")).to_be_visible()
    log_step("Fork count visible")

    expect(page.locator('span[data-content="README"]')).to_be_visible()
    log_step("README section rendered")

@pytest.mark.ui
def test_code_navigation_and_typescript_file(page):
    """Navigate through code repository and verify file display."""
    page.goto(REPO_UI_URL)

    log_step("Clicking src folder")
    page.get_by_role("link", name="src, (Directory)").first.click()    
    page.wait_for_url("**/src")
    log_step("Navigated to src directory")

    breadcrumb_src = page.get_by_role("heading", name="src")
    expect(breadcrumb_src).to_be_visible()
    log_step("Breadcrumb 'src' visible")

    log_step("Finding TypeScript file")
    ts_href = page.locator("a[aria-label$='.ts, (File)']").first.get_attribute("href")
    assert ts_href is not None
    log_step(f"Opening file: {ts_href}")
    page.goto(f"https://github.com{ts_href}")
    log_step("File page loaded")

    code = page.locator("div.react-code-lines >> div.react-code-text").first
    expect(code).to_be_visible()
    log_step("Code content visible")
    line_numbers = page.locator("div.react-line-number")
    expect(line_numbers.first).to_be_visible()
    line_count = line_numbers.count()
    assert line_count > 0
    log_step(f"Line numbers visible ({line_count} lines)")

@pytest.mark.ui
def test_repo_stats_and_metadata(page):
    """Verify repository statistics and metadata are displayed."""
    page.goto(REPO_UI_URL)
    log_step("Page loaded")

    about_section = page.locator("div.BorderGrid.about-margin")
    expect(about_section).to_be_visible()
    log_step("About section found")

    description = about_section.locator("p").filter(has_text=re.compile(".+")).first

    expect(description).to_be_visible()
    assert description.inner_text().strip() != ""
    desc_text = description.inner_text().strip()
    log_step(f"Description: {desc_text[:60]}...")

    license_link = about_section.locator("a").filter(has_text="license")

    assert license_link.count() > 0, "License Information not found"
    log_step(f"License info found")

    topics = page.locator("a.topic-tag")
    assert topics.count() > 0, "Topics/tags not found"
    log_step(f"Topics/tags found ({topics.count()} tags)")







