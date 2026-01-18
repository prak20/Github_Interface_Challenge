from loguru import logger
from playwright.sync_api import Page, expect, Playwright
import pytest
import os
import sys
from typing import Generator
from config import REPO_API_BASE, LOG_FILE

# Setup logging - file and console
os.makedirs("logs", exist_ok=True)

# Clear previous log file by truncating
open(LOG_FILE, 'w').close()

logger.remove()
# File logging with rotation
logger.add(f"{LOG_FILE}", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", rotation="5 MB", enqueue=True, serialize=False)
# Console logging for real-time visibility
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", colorize=True)

def pytest_configure(config):
    """Log which browser will be used."""
    browser = config.getoption("--browser")
    logger.info(f"Browser selected: {browser}")

@pytest.fixture(scope="session")
def browser_context(playwright: Playwright,request):
    """Create a browser context - browser selected via --browser option."""
    browser_name = request.config.getoption("--browser")
    logger.info(f"Launching {browser_name} browser")
    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False, slow_mo=500)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=False, slow_mo=500)
    else:
        logger.warning(f"Unknown browser '{browser_name}', using chromium")
    browser = playwright.firefox.launch(headless=False, slow_mo=500)
    context = browser.new_context()
    yield context
    context.close()
    browser.close()

@pytest.fixture(scope="function")
def page(browser_context):
    """Create a new page for each test."""
    page = browser_context.new_page()
    logger.info("New page opened for test isolation")
    yield page
    page.close()
    logger.info("Page closed")

@pytest.fixture(autouse=True)
def log_test_start_and_end(request):
    """Announce test start and end"""
    logger.info(f"Starting test: {request.node.name}")
    yield
    logger.info(f"Finished test: {request.node.name}")

@pytest.fixture(scope="session")
def api_context(playwright):
    """Create an API request context for GitHub API."""
    context = playwright.request.new_context(
        base_url=f"{REPO_API_BASE}"
    )
    yield context
    context.dispose()

