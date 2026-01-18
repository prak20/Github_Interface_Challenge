from loguru import logger
from playwright.sync_api import Page, expect, sync_playwright
import pytest
import os
import sys

# Setup logging
os.makedirs("logs", exist_ok=True)
logger.remove()
logger.add("logs/tests.log",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", rotation="5 MB", enqueue=True, serialize=False)



@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser_context):
    context = browser_context.new_context()
    page = context.new_page()
    logger.info("New page opened for test isolation")
    yield page
    page.close()
    logger.info("Page closed")

@pytest.fixture(autouse=True)
def log_test_start_and_end(request):
    """Announce test start and end, we do."""
    logger.info(f"Starting test: {request.node.name}")
    yield
    logger.info(f"Finished test: {request.node.name}")


@pytest.fixture(scope="session")
def api_context(playwright):
    """
    API ke liye ek context banana hai,
    reuse karna powerful hota hai.
    """
    context = playwright.request.new_context(
        base_url="https://api.github.com"
    )
    yield context
    context.dispose()

