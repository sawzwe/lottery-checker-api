# Tests

This directory contains test files and verification scripts.

## Files

- `test_api.py` - Comprehensive API endpoint testing
  - Tests all lottery API endpoints
  - Validates response formats
  - Checks error handling

- `test_api_simple.py` - Basic API connectivity test
  - Quick health check test
  - Basic endpoint verification

- `test_setup.py` - Environment and configuration verification
  - Validates environment variables
  - Tests database connectivity
  - Checks Supabase configuration

## Usage

### Run API tests:

```bash
# Make sure API is running first
python run_api.py

# Then run tests in another terminal
python tests/test_api.py
```

### Quick connectivity test:

```bash
python tests/test_api_simple.py
```

### Verify your setup:

```bash
python tests/test_setup.py
```

## Test Coverage

- ✅ Root endpoint (`/`)
- ✅ Health check (`/health`)
- ✅ Get latest draw (`/api/th/v1/lottery/draws/latest`)
- ✅ Get all draws (`/api/th/v1/lottery/draws`)
- ✅ Get draw by date (`/api/th/v1/lottery/draws/{date}`)
- ✅ Check lottery numbers (`/api/th/v1/lottery/check`)
- ✅ Search draws (`/api/th/v1/lottery/search`)

## Requirements

- API server must be running on `http://localhost:8000`
- Database must be populated with lottery data
- Environment variables must be configured 