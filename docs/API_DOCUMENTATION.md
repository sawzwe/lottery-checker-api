# Lottery Checker API Documentation

## Base URL
```
http://localhost:8000
```

## Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Thai Lottery Endpoints

### Get All Draws
**GET** `/api/th/v1/lottery/draws`

Get paginated list of lottery draws.

**Parameters:**
- `page` (int): Page number (default: 1)
- `size` (int): Items per page, max 100 (default: 50)

**Example:**
```bash
curl -X GET "http://localhost:8000/api/th/v1/lottery/draws?page=1&size=10"
```

### Get Latest Draw
**GET** `/api/th/v1/lottery/draws/latest`

Get the most recent lottery draw.

**Example:**
```bash
curl -X GET "http://localhost:8000/api/th/v1/lottery/draws/latest"
```

### Get Draw by Date
**GET** `/api/th/v1/lottery/draws/{date}`

Get lottery draw for specific date.

**Parameters:**
- `date` (string): Date in YYYY-MM-DD format

**Example:**
```bash
curl -X GET "http://localhost:8000/api/th/v1/lottery/draws/2024-12-16"
```

### Check Lottery Numbers
**POST** `/api/th/v1/lottery/check`

Check lottery numbers for winnings.

**Request Body:**
```json
{
  "numbers": ["123456", "789012"],
  "date": "2024-12-16"  // Optional
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/th/v1/lottery/check" \
  -H "Content-Type: application/json" \
  -d '{"numbers": ["97863", "123456"]}'
```

### Search Draws
**GET** `/api/th/v1/lottery/search`

Search lottery draws with date filters.

**Parameters:**
- `start_date` (string): Start date YYYY-MM-DD (optional)
- `end_date` (string): End date YYYY-MM-DD (optional)
- `page` (int): Page number (default: 1)
- `size` (int): Items per page, max 100 (default: 50)

**Example:**
```bash
curl -X GET "http://localhost:8000/api/th/v1/lottery/search?start_date=2024-01-01&end_date=2024-12-31"
```

---

## System Endpoints

### Root
**GET** `/`

Get API information and available endpoints.

### Health Check
**GET** `/health`

Check API health and database connectivity.

---

## Prize Structure (Thai Lottery)

| Prize Type | Amount |
|------------|--------|
| 1st Prize | ฿6,000,000 |
| Around 1st | ฿100,000 |
| 2nd Prize | ฿200,000 |
| 3rd Prize | ฿80,000 |
| 4th Prize | ฿40,000 |
| 5th Prize | ฿20,000 |
| 3-digit Prizes | ฿4,000 |
| 2-digit Prize | ฿2,000 |

---

## Response Format

All endpoints return responses in this format:

```json
{
  "success": true,
  "message": "Operation completed",
  "data": { /* response data */ },
  "error": null
}
```

---

## Error Codes

- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

---

## Database Info

- **Total Records:** 429 draws
- **Date Range:** 2022-12-16 to 2024-12-16
- **Country:** Thailand (TH)

---

## Quick Start

1. Start API: `python run_api.py`
2. Visit docs: http://localhost:8000/docs
3. Test endpoint: `curl http://localhost:8000/health` 

# Lucas Document Update
# API Key Generation & Storage

## Generate API Keys
Generate a unique API key for each client.

**Script:** `key_generator.py`

**Example Output:**
Generated API keys:
Name: client1, Key: b2e8f03e2fdf1c88a7d7c2f2e7e4c8e2...
Name: client2, Key: a4f87c1b9d8a4eebcfa5e3a9d1a7f22b...
Name: client3, Key: 8c1e2d4b7a9f0c5d3e6b1a2f4e8d7c9b...

yaml
ကူးယူရန်
ပြင်ဆင်ရန်

---

## Store API Keys
Save the generated keys in **Supabase** in a table named `api_keys`.

| id  | api_key                              | client_name | active | created_at          |
|-----|--------------------------------------|-------------|--------|---------------------|
| 1   | b2e8f03e2fdf1c88a7d7c2f2e7e4c8e2    | client1     | ✅     | 2025-07-17 12:00:00 |

You can query this table in your code to validate incoming requests.

---

## Validate API Key
On each request to your API, validate the key by checking the `X-API-Key` header.

**Header:**
X-API-Key: <client-api-key>

vbnet
ကူးယူရန်
ပြင်ဆင်ရန်

If the key is invalid or missing, the server responds with:

- `401 Unauthorized`

