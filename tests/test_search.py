import re
import pytest
from playwright.sync_api import expect
from config import REPO_UI_URL
from helpers import log_step

@pytest.mark.search
def test_search_repository_happy_path(page):
    """Test successful repository search functionality."""
    log_step("Opening GitHub home page")
    page.goto("https://github.com")

    log_step("Opening search with keyboard shortcut")
    page.keyboard.press("/")

    search_input = page.locator('input[name="query-builder-test"]')
    expect(search_input).to_be_visible()
    log_step("Search input visible")

    log_step("Typing search query: microsoft vscode")
    search_input.fill("microsoft vscode")
    search_input.press("Enter")

    log_step("Waiting for search results page")
    page.wait_for_url("**/search**")
    expect(page).to_have_url(re.compile("search"))
    log_step("Search results loaded")

    result = page.get_by_role("link", name="microsoft/vscode", exact=True)
    expect(result).to_be_visible()
    log_step("Found microsoft/vscode in results")

@pytest.mark.search
@pytest.mark.parametrize("invalid_data", [
    "asdkjhaskdjh123","xyzabc999xyz","nonexistentrepo12345invalidquery"
])
def test_search_no_results(page, invalid_data):
    """Test search with no matching results."""
    log_step("Opening GitHub home page")
    page.goto("https://github.com")

    log_step("Opening search")
    page.keyboard.press("/")
    log_step(f"Typing invalid search: {invalid_data}")
    page.locator('input[name="query-builder-test"]').fill(invalid_data)
    page.keyboard.press("Enter")

    log_step("Checking for 'no results' message")
    no_results_heading = page.get_by_role(
        "heading",
        name=re.compile("did not match any repositories", re.IGNORECASE)
    )

    expect(no_results_heading).to_be_visible()
    log_step("No results message displayed")