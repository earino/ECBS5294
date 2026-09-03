# API Pipeline Quick Reference Card

**ECBS5294 - Data Science 2: Working with Data**

**Purpose:** Production patterns for building robust API ingestion pipelines.

---

## Core Pattern (From Class)

**Basic API request with timeout and error handling:**

```python
import requests
import json

# Make HTTP GET request
response = requests.get(
    "https://api.example.com/data",
    params={'limit': 100},
    timeout=10  # Always set timeout!
)

# Check for HTTP errors
response.raise_for_status()

# Parse JSON
data = response.json()
```

**Why timeout matters:** Without a timeout, your script can hang forever if the API is slow or unresponsive.

---

## Production Enhancements

### 1. Connection Pooling with `requests.Session()`

**Problem:** Creating a new connection for every request is slow (especially for multiple requests to the same API).

**Solution:** Use `Session()` to reuse connections (60% faster for multiple requests).

```python
import requests

# Create session (reuses connections)
session = requests.Session()

# Make multiple requests (faster!)
for page in range(1, 11):
    response = session.get(
        "https://api.example.com/data",
        params={'page': page, 'limit': 100},
        timeout=10
    )
    response.raise_for_status()
    data = response.json()
    # Process data...

# Clean up
session.close()
```

**When to use:** Any time you're making more than one request to the same API.

---

### 2. Automatic Retry with `tenacity`

**Problem:** APIs occasionally fail due to transient issues (network blip, server overload, rate limit).

**Solution:** Automatically retry failed requests with exponential backoff.

```python
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),  # Try 3 times
    wait=wait_exponential(multiplier=1, min=2, max=10),  # Wait 2s, 4s, 8s
    retry=retry_if_exception_type((requests.RequestException, requests.Timeout))
)
def fetch_data(url, params):
    """Fetch data with automatic retry."""
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

# Use it
data = fetch_data("https://api.example.com/data", {'limit': 100})
```

**Install (optional, not a course dependency):** `uv add tenacity`

**When to use:** Production pipelines where reliability is critical.

---

### 3. Rate Limiting (Respect API Limits)

**Problem:** Most APIs have rate limits (e.g., 100 requests per minute). Exceeding them gets you blocked.

**Solution:** Add delays between requests.

```python
import time
import requests

API_URL = "https://api.example.com/data"
RATE_LIMIT_DELAY = 0.6  # 0.6 seconds = 100 requests/minute

for page in range(1, 101):
    response = requests.get(API_URL, params={'page': page}, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Process data...

    # Wait before next request
    time.sleep(RATE_LIMIT_DELAY)
```

**Better approach:** Use `ratelimit` library for more sophisticated control.

```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)  # 100 calls per 60 seconds
def fetch_data(url, params):
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
```

**Install (optional, not a course dependency):** `uv add ratelimit`

---

### 4. Authentication (API Keys, OAuth)

**Problem:** Many APIs require authentication.

**Solution:** Pass credentials securely.

**API Key in Header (most common):**
```python
import requests
import os

API_KEY = os.environ.get('API_KEY')  # Never hardcode keys!

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

response = requests.get(
    "https://api.example.com/data",
    headers=headers,
    timeout=10
)
```

**API Key in Query Parameter:**
```python
params = {
    'api_key': os.environ.get('API_KEY'),
    'limit': 100
}

response = requests.get(
    "https://api.example.com/data",
    params=params,
    timeout=10
)
```

**Security rules:**
- ✅ Store keys in environment variables (`os.environ`)
- ✅ Use `.env` files (with `python-dotenv`)
- ✅ Add `.env` to `.gitignore`
- ❌ NEVER hardcode keys in scripts
- ❌ NEVER commit keys to git

---

### 5. Pagination (Fetching All Data)

**Problem:** APIs return data in pages (e.g., 100 records per request). You need to loop through all pages.

**Pattern A: Offset-based pagination**
```python
import requests

all_data = []
offset = 0
limit = 100

while True:
    response = requests.get(
        "https://api.example.com/data",
        params={'offset': offset, 'limit': limit},
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    records = data['results']
    all_data.extend(records)

    # Check if we got all data
    if len(records) < limit:
        break

    offset += limit

print(f"Fetched {len(all_data)} total records")
```

**Pattern B: Cursor-based pagination (Twitter, GitHub)**
```python
import requests

all_data = []
next_cursor = None

while True:
    params = {'limit': 100}
    if next_cursor:
        params['cursor'] = next_cursor

    response = requests.get("https://api.example.com/data", params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    all_data.extend(data['results'])

    # Check for next page
    next_cursor = data.get('next_cursor')
    if not next_cursor:
        break

print(f"Fetched {len(all_data)} total records")
```

---

### 6. Caching API Responses

**Problem:** Fetching the same data repeatedly is slow and wastes API quota.

**Solution:** Cache responses to disk.

```python
import requests
import json
import os
from datetime import datetime, timedelta

CACHE_DIR = "cache/"
CACHE_EXPIRY = timedelta(hours=24)

def fetch_with_cache(url, params):
    """Fetch data with file-based caching."""
    # Create cache key from URL + params
    cache_key = f"{url}_{str(params)}".replace('/', '_').replace(':', '_')
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")

    # Check if cached file exists and is recent
    if os.path.exists(cache_file):
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))
        if file_age < CACHE_EXPIRY:
            print(f"Using cached data (age: {file_age})")
            with open(cache_file) as f:
                return json.load(f)

    # Fetch fresh data
    print("Fetching fresh data from API...")
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Save to cache
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(data, f)

    return data

# Use it
data = fetch_with_cache("https://api.example.com/data", {'limit': 100})
```

**Better approach:** Use `requests-cache` library.

```python
import requests_cache

# Setup cache (SQLite backend)
requests_cache.install_cache('api_cache', expire_after=3600)  # 1 hour

# Use requests normally - automatic caching!
response = requests.get("https://api.example.com/data", timeout=10)
data = response.json()
```

**Install (optional, not a course dependency):** `uv add requests-cache`

---

## Complete Production Example

**Combining all patterns:**

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tenacity import retry, stop_after_attempt, wait_exponential
from ratelimit import limits, sleep_and_retry
import os
import json

class ProductionAPIClient:
    """Production-ready API client with all best practices."""

    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.session = requests.Session()

        # Add retry logic for transient failures
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Add authentication if provided
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })

    @sleep_and_retry
    @limits(calls=100, period=60)  # Rate limit: 100/minute
    def get(self, endpoint, params=None):
        """GET request with rate limiting."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def close(self):
        """Clean up session."""
        self.session.close()

# Usage
client = ProductionAPIClient(
    base_url="https://api.example.com",
    api_key=os.environ.get('API_KEY')
)

try:
    data = client.get("products", params={'limit': 100})
    print(f"Fetched {len(data)} products")
finally:
    client.close()
```

---

## Error Handling Best Practices

**Always handle these errors:**

```python
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError

try:
    response = requests.get(
        "https://api.example.com/data",
        params={'limit': 100},
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

except Timeout:
    print("❌ Request timed out (API too slow)")
    # Option: Use cached data or retry

except ConnectionError:
    print("❌ Network connection failed")
    # Option: Use cached data or fail gracefully

except HTTPError as e:
    if e.response.status_code == 404:
        print("❌ Endpoint not found")
    elif e.response.status_code == 429:
        print("❌ Rate limit exceeded")
    elif e.response.status_code >= 500:
        print("❌ Server error (API is down)")
    else:
        print(f"❌ HTTP error: {e}")

except ValueError:
    print("❌ Invalid JSON response")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

---

## Logging for Production

**Problem:** You need to debug failures in production pipelines.

**Solution:** Use Python's `logging` module.

```python
import requests
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_data(url, params):
    """Fetch data with logging."""
    logger.info(f"Fetching: {url} with params: {params}")

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Success: Fetched {len(data)} records")
        return data

    except requests.Timeout:
        logger.error("Request timed out")
        raise

    except requests.HTTPError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        raise

    except Exception as e:
        logger.exception("Unexpected error")
        raise

# Use it
data = fetch_data("https://api.example.com/data", {'limit': 100})
```

---

## Testing API Pipelines

**Use `responses` library to mock API calls in tests:**

```python
import requests
import responses

@responses.activate
def test_fetch_data():
    """Test API fetch with mocked response."""
    # Mock the API
    responses.add(
        responses.GET,
        "https://api.example.com/data",
        json={'results': [{'id': 1, 'name': 'Test'}]},
        status=200
    )

    # Test your function
    response = requests.get("https://api.example.com/data")
    data = response.json()

    assert len(data['results']) == 1
    assert data['results'][0]['name'] == 'Test'

# Run test
test_fetch_data()
```

**Install (optional, not a course dependency):** `uv add responses`

---

## Decision Framework

**Ask yourself:**

1. **How many requests am I making?**
   - Single request → Basic `requests.get()`
   - Multiple requests → Use `requests.Session()`

2. **How reliable is the API?**
   - Very reliable → Basic error handling
   - Occasionally flaky → Add retry logic (`tenacity`)

3. **Are there rate limits?**
   - No limits → No rate limiting needed
   - Limited → Add `time.sleep()` or `ratelimit`

4. **Do I need authentication?**
   - Public API → No auth
   - Private API → Add API key or OAuth

5. **Is this a one-time script or production pipeline?**
   - One-time → Keep it simple
   - Production → Add logging, caching, monitoring

---

## Common Mistakes

❌ **Don't do this:**
- No timeout (can hang forever)
- No error handling (crashes on network issues)
- Hardcoded API keys
- Making 1000 requests in a loop without rate limiting
- Fetching same data repeatedly without caching

✅ **Do this instead:**
- Always set `timeout`
- Handle `Timeout`, `ConnectionError`, `HTTPError`
- Store API keys in environment variables
- Use `Session()` and rate limiting
- Cache responses to disk

---

## Additional Resources

**Libraries:**
- `requests` - HTTP library (core): https://requests.readthedocs.io/
- `tenacity` - Retry logic: https://tenacity.readthedocs.io/
- `ratelimit` - Rate limiting: https://github.com/tomasbasham/ratelimit
- `requests-cache` - Caching: https://requests-cache.readthedocs.io/
- `responses` - Testing: https://github.com/getsentry/responses

**Learning:**
- "Requests: HTTP for Humans" tutorial: https://requests.readthedocs.io/en/latest/user/quickstart/
- Real Python guide: https://realpython.com/python-requests/
- API best practices: https://www.freecodecamp.org/news/rest-api-best-practices/

**DuckDB + APIs:**
- Ingest JSON directly: `SELECT * FROM read_json_auto('https://api.example.com/data.json')`
- Persist normalized tables: `CREATE TABLE products AS SELECT * FROM products_df`

---

**Remember:** Start simple (basic `requests.get()`) and add complexity only when you need it. Production patterns are tools, not requirements for every script.
