# Lottery Checker API

A comprehensive multi-country lottery checking system with REST API, data management tools, and historical analysis capabilities.

## 🎯 Features

- **🔍 Number Checking**: Check lottery numbers against historical draws
- **📊 API Access**: RESTful API with interactive documentation  
- **🌍 Multi-Country Ready**: Structured for easy expansion (Thailand currently supported)
- **📈 Historical Data**: 429+ lottery draws from 2022-2024
- **🛠️ Data Management**: Tools for uploading and managing lottery data
- **✅ Comprehensive Testing**: Full test suite for API and data integrity

## 📁 Project Structure

```
lottery-checker-api/
├── app/                      # FastAPI application
│   ├── controllers/          # API controllers
│   ├── core/                 # Core functionality (database, etc.)
│   ├── models/               # Pydantic models
│   ├── routes/               # API routes
│   └── services/             # Business logic
├── config/                   # Configuration files
│   ├── config.py            # Main configuration
│   └── README.md            # Config documentation
├── datasets/                 # Data files
├── docs/                     # Documentation
│   ├── API_DOCUMENTATION.md # API reference
│   └── README.md            # Documentation index
├── scripts/                  # Data management scripts
│   ├── lottery_uploader.py  # Core upload functionality
│   ├── upload_lottery_data.py # CLI upload script
│   └── README.md            # Scripts documentation
├── static/                   # Static files (HTML, CSS)
├── tests/                    # Test files
│   ├── test_api.py          # API endpoint tests
│   ├── test_api_simple.py   # Basic connectivity tests
│   ├── test_setup.py        # Environment verification
│   └── README.md            # Test documentation
├── tools/                    # Database setup tools
│   ├── create_table.py      # Automated table creation
│   ├── create_table.sql     # Manual SQL setup
│   └── README.md            # Tools documentation
├── requirements.txt          # Python dependencies
├── run_api.py               # Server launcher
└── README.md                # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Supabase Credentials

**✅ You're all set!** Your environment variables are already configured:

**URLs (will use in this order):**
- `SUPERBASE_PROJECT_URL` ✓ (you have this!)
- `SUPABASE_URL` (fallback)

**API Keys (will use in this order):**
- `API_SERVICE_ROLE_SUPERBASE` ✓ (best for data operations)
- `API_JWT_KEY` ✓ (you have this!)
- `API_KEYS_SUPERBASE` ✓ (fallback)

**Your complete environment setup:**
- `API_SERVICE_ROLE_SUPERBASE` ✓
- `API_JWT_KEY` ✓  
- `API_KEYS_SUPERBASE` ✓
- `SUPERBASE_PROJECT_URL` ✓
- `OPEN_AI_KEY` ✓
- `DB_PASSWORD` ✓

**No additional configuration needed!** The system will automatically use your existing variables.

### 3. Run the API

Start the lottery checker API server:

```bash
python run_api.py
```

The API will be available at:
- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **API Documentation**: http://localhost:8000/redoc

#### API Endpoints

```
# Thai Lottery Endpoints
GET  /api/th/v1/lottery/draws           # Get all draws (paginated)
GET  /api/th/v1/lottery/draws/latest    # Get latest draw
GET  /api/th/v1/lottery/draws/{date}    # Get draw by date
POST /api/th/v1/lottery/check           # Check lottery numbers
GET  /api/th/v1/lottery/search          # Search draws with filters

# System Endpoints  
GET  /                                  # API information
GET  /health                            # Health check
```

### 4. Test Your Setup

Run the setup verification script to check your configuration:
```bash
python tests/test_setup.py
```

This will verify:
- Your environment variables are loaded correctly
- Your Supabase connection works
- Whether the database table exists

### 5. Create Database Table

**🚨 CRITICAL STEP - Required before uploading data!**

**Option A: Use automated script**
```bash
python tools/create_table.py
```

**Option B: Copy SQL from file**
```bash
# Open tools/create_table.sql and copy all the SQL code
# Then paste it in your Supabase SQL Editor
```

**Option C: Copy SQL directly**
Go to your Supabase dashboard → SQL Editor and run:

```sql
CREATE TABLE IF NOT EXISTS lottery_draws (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    prize_1st VARCHAR(10),
    prize_pre_3digit TEXT[],
    prize_sub_3digits TEXT[],
    prize_2digits INTEGER,
    nearby_1st TEXT[],
    prize_2nd TEXT[],
    prize_3rd TEXT[],
    prize_4th TEXT[],
    prize_5th TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_lottery_draws_date ON lottery_draws(date);
```

**Verify creation:**
- You should see "Success" message
- The table should appear in your Supabase Tables list

## Usage

### Upload CSV Data

**Simple Method:**
```bash
python scripts/upload_lottery_data.py your_data.csv
```

**Or run interactively:**
```bash
python scripts/upload_lottery_data.py
```

**Advanced Method:**
```bash
# Use the uploader class directly in Python
from scripts.lottery_uploader import LotteryUploader
uploader = LotteryUploader()
uploader.upload_csv("your_data.csv")
```

### Test with Sample Data

A sample CSV file is included for testing:
```bash
python scripts/upload_lottery_data.py datasets/sample_lottery_data.csv
```

The script will:
1. **Verify table exists** (fails immediately if not)
2. Check each record against existing data
3. Skip duplicate records (based on date)
4. Upload only new records
5. **Verify each upload** in the database
6. Provide detailed summary with success/failure status

**🔒 Data Integrity Features:**
- ✅ **Verification after upload** - confirms data actually reached database
- ✅ **Atomic operations** - each record is fully verified before continuing
- ✅ **Clear error reporting** - shows exactly what succeeded/failed
- ✅ **No false positives** - only shows success when data is actually in database

### CSV Format

Your CSV file should have these columns:
- `date`: Date in YYYY-MM-DD format
- `prize_1st`: First prize number (string)
- `prize_pre_3digit`: Array of 3-digit pre-numbers (as string representation of Python list)
- `prize_sub_3digits`: Array of 3-digit sub-numbers (as string representation of Python list)
- `prize_2digits`: 2-digit prize number (integer)
- `nearby_1st`: Array of nearby first prize numbers (as string representation of Python list)
- `prize_2nd` through `prize_5th`: Arrays of prize numbers (as string representations of Python lists)

### Example CSV Row

```csv
date,prize_1st,prize_pre_3digit,prize_sub_3digits,prize_2digits,nearby_1st,prize_2nd,prize_3rd,prize_4th,prize_5th
2024-12-16,097863,"['290', '742']","['339', '881']",21,"['097862', '097864']","['077335', '142161']","['132601', '164003']","['005170', '142726']","['000720', '126272']"
```

## Features

- **Duplicate Prevention**: Automatically checks for existing records by date
- **Error Handling**: Continues processing even if individual records fail
- **Progress Tracking**: Shows real-time upload progress
- **Summary Report**: Provides detailed upload statistics
- **Array Field Parsing**: Properly handles string representations of Python lists

## Error Handling

The script includes robust error handling:
- Skips malformed records and continues processing
- Validates Supabase connection before starting
- Provides detailed error messages for troubleshooting
- Maintains upload statistics for failed records

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase anon key | 