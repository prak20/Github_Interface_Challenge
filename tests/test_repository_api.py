import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext
from helpers import log_step
from config import REACT_REPO, NONEXISTENT_REPO, ISSUE_URL,REACT_CONTENT_REPO

@pytest.mark.api
def test_get_react_repository(api_context):
    """Fetch React repository and verify it exists with correct metadata."""
    log_step("Testing: GET /repos/facebook/react")
    response = api_context.get(f"/{REACT_REPO}")

    assert response.status == 200
    log_step(f"Status: {response.status}")

    data = response.json()
    assert data["name"] == "react"
    assert data["owner"]["login"] == "facebook"
    log_step(f"Repository: {data['name']}, Owner: {data['owner']['login']}")
    
    assert data["stargazers_count"] > 100000
    log_step(f"Stars: {data['stargazers_count']:,}")
    
    assert data["private"] is False
    log_step(f"Visibility: Public")

    headers = response.headers
    assert "x-ratelimit-limit" in headers
    assert "x-ratelimit-remaining" in headers
    log_step(f"Rate Limit: {headers.get('x-ratelimit-limit')} | Remaining: {headers.get('x-ratelimit-remaining')}")

@pytest.mark.api
def test_get_react_repository_contents(api_context):
    """Verify repository contents endpoint returns files list."""
    log_step("Testing: GET /repos/facebook/react/contents")
    response = api_context.get(f"/{REACT_CONTENT_REPO}")

    assert response.status == 200
    log_step(f"Status: {response.status}")

    data = response.json()
    assert isinstance(data, list)
    log_step(f"Content items: {len(data)}")

    names = [item["name"] for item in data]
    assert "README.md" in names
    assert "package.json" in names
    log_step(f"Found: README.md, package.json")

@pytest.mark.api
def test_non_existent_repository(api_context):
    """Verify non-existent repository returns 404 error."""
    log_step("Testing: GET /repos/microsoft/nonexistent-repo-12345")
    response = api_context.get(f"/{NONEXISTENT_REPO}")

    assert response.status == 404
    log_step(f"Status: {response.status} (expected 404)")
    assert "Not Found" in response.json().get("message", "")
    log_step(f"Error message: {response.json().get('message')}")

@pytest.mark.api
def test_github_api_rate_limit_headers(api_context):
    """Verify rate limit headers are present in API responses."""
    log_step("Testing: Rate limit headers")
    response = api_context.get(f"/{REACT_REPO}")

    assert response.status == 200

    headers = response.headers

    assert "x-ratelimit-limit" in headers
    assert "x-ratelimit-remaining" in headers

@pytest.mark.api
def test_invalid_issue_returns_404(api_context):
    """Verify invalid issue endpoint returns 404 error."""
    log_step("Testing: GET /repos/facebook/react/issues/999999999")
    response = api_context.get(f"/{ISSUE_URL}")

    assert response.status == 404
    log_step(f"Status: {response.status} (expected 404 for invalid issue)")