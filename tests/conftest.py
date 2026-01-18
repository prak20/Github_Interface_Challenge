from loguru import logger
from playwright.sync_api import Page, expect, Playwright
import pytest
import os
import sys
import asyncio
from typing import Generator
from config import REPO_API_BASE,LOG_FILE

# Setup logging - file and console
os.makedirs("logs", exist_ok=True)
logger.remove()
# File logging with rotation
logger.add(f"{LOG_FILE}", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", rotation="5 MB", enqueue=True, serialize=False)
# Console logging for real-time visibility
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", colorize=True)

@pytest.fixture(scope="session")
def browser_context(playwright: Playwright):
    """Create a browser context from the playwright instance."""
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
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
        base_url=f"{REPO_API_BASE}"
    )
    yield context
    context.dispose()

