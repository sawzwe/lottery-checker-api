# Scripts

This directory contains utility scripts for data management and operations.

## Files

- `lottery_uploader.py` - Core data upload functionality
  - CSV parsing and validation
  - Duplicate detection
  - Batch upload to Supabase
  - Data verification

- `upload_lottery_data.py` - Simple command-line interface for data upload
  - Easy-to-use script for uploading CSV files
  - Error handling and progress reporting

## Usage

### Upload lottery data from CSV:

```bash
# Interactive mode
python scripts/upload_lottery_data.py

# Command line mode
python scripts/upload_lottery_data.py path/to/your/data.csv
```

### Use uploader class directly:

```python
from scripts.lottery_uploader import LotteryUploader

uploader = LotteryUploader()
success = uploader.upload_csv("data.csv")
```

## Data Format

CSV files should have columns:
- `date` - Lottery draw date (YYYY-MM-DD)
- `prize_1st` - First prize number
- `prize_pre_3digit` - Pre 3-digit numbers (as string list)
- `prize_sub_3digits` - Sub 3-digit numbers (as string list)
- `prize_2digits` - 2-digit number
- `nearby_1st` - Numbers around first prize
- `prize_2nd` to `prize_5th` - Other prize categories 