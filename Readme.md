# GitHub Interface Testing Challenge

Automated test suite for GitHub's public interface using Python, Pytest, and Playwright.

## Setup

### Clone from GitHub

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/GitHub_Interface_Challenge.git

# Navigate to project directory
cd Github_Interface_Challenge

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

### Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Running Tests

### Quick Start
```bash
pytest tests/ -v --html=report.html --self-contained-html
```

This will:
- Open a browser window (not headless)
- Execute tests one by one with 500ms delays between actions
- Log each step to console with timestamps
- Generate an HTML report at `report.html`

### Run Specific Tests
```bash
# UI tests only
pytest tests/test_repository_ui.py -v

# API tests only
pytest tests/test_repository_api.py -v

# Search tests only
pytest tests/test_search.py -v

# Single test
pytest tests/test_repository_ui.py::test_repo_page_loads -v

# Show console output
pytest tests/ -v -s
```

### Change Browser
```bash
pytest tests/ --browser firefox
pytest tests/ --browser webkit
```

## What Tests Do

### UI Tests (test_repository_ui.py) 
1. **test_repo_page_loads** - Verifies repository page loads with correct name, owner, stars, forks, and README
2. **test_code_navigation** - Verifies clicking folders navigates correctly and files display with syntax highlighting
3. **test_repository_metadata** - Verifies about section, license, and topics are visible

### API Tests (test_repository_api.py)
1. **test_react_repo_get** - Verifies React repository retrieval and validation (status 200, correct data)
2. **test_repository_contents** - Verifies repository contents endpoint returns array with expected files
3. **test_nonexistent_repo** - Verifies 404 response for non-existent repositories
4. **test_rate_limit_headers** - Verifies rate limit headers are present in response
5. **test_invalid_issue** - Verifies 404 response for invalid issue IDs

### Search Tests (test_search.py)
1. **test_happy_path_search** - Verifies search functionality and correct results display
2. **test_no_results_search** - Verifies appropriate message when no results found

## Logging

Tests log to two places:

**Console** - Real-time output with timestamps:
```
2026-01-18 10:30:45 | INFO | Starting test: test_repo_page_loads
2026-01-18 10:30:47 | INFO | Loading vscode repo
2026-01-18 10:30:50 | INFO | Verified repository loaded successfully
```

**File** - Persistent log at `logs/tests.log`:
- Each test execution logged with timestamp
- Log file rotates at 5 MB
- Clears before each test run

## Project Structure

```
Github_Interface_Challenge/
├── config.py                 # Global configuration (API URLs, repos)
├── pytest.ini               # Pytest settings
├── requirements.txt         # Python dependencies
├── Readme.md               # Documentation
├── report.html             # Generated test report
├── logs/                   # Test logs
├── results/               # Test results
└── tests/
    ├── conftest.py        # Fixtures and pytest hooks
    ├── config.py          # Test data and endpoints
    ├── helpers.py         # Helper functions
    ├── test_repository_ui.py      # UI tests
    ├── test_repository_api.py     # API tests
    └── test_search.py             # Search tests
```

## Browser Settings

Tests run with:
- **Visible browser window** (not headless)
- **500ms delay** between actions for visibility
- **Auto-waiting** for elements using Playwright locators
- **Fresh page** for each test (test isolation)

## Test Reports

After running tests, open `report.html` to see:
- Overall summary (passed/failed/skipped)
- Individual test results with execution times
- Error details if any tests failed

## Dependencies

- `pytest` - Test framework
- `pytest-playwright` - Playwright plugin for pytest
- `playwright` - Browser automation
- `requests` - HTTP client for API tests
- `loguru` - Logging
- `pytest-html` - HTML report generation

## Troubleshooting

**Tests won't run:**
```bash
pytest --version  # Verify pytest is installed
playwright install  # Ensure browsers are installed
```

**Browser won't open:**
- Verify `headless=False` in `conftest.py` (default)
- Run `playwright install` to install browsers

**API tests failing:**
- Check internet connection
- Verify GitHub is accessible
- API rate limits: GitHub allows 60 requests/hour for unauthenticated users

**Logs not appearing:**
- Create logs directory: `mkdir logs`
- Check file permissions
- Console output shows in terminal in real-time

## Notes

- Each test gets a fresh page - no shared state between tests
- Tests use Playwright's built-in locators and auto-waiting
- Pytest fixtures manage browser setup and teardown
- Log files clear before each test run
