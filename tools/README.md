# Tools

This directory contains database setup and management tools.

## Files

- `create_table.py` - Automated database table creation
  - Creates lottery_draws table in Supabase
  - Sets up proper indexes
  - Handles error cases gracefully

- `create_table.sql` - Raw SQL for manual table creation
  - SQL commands for table structure
  - Index creation statements
  - Can be run directly in Supabase SQL editor

## Usage

### Automated table creation:

```bash
python tools/create_table.py
```

### Manual table creation:

1. Open your Supabase dashboard
2. Go to SQL Editor
3. Copy and run the contents of `create_table.sql`

## Database Schema

The `lottery_draws` table includes:

- `id` - Primary key (auto-increment)
- `date` - Draw date (unique)
- `prize_1st` - First prize number
- `prize_pre_3digit` - Array of pre 3-digit numbers
- `prize_sub_3digits` - Array of sub 3-digit numbers
- `prize_2digits` - 2-digit number
- `nearby_1st` - Array of numbers around first prize
- `prize_2nd` to `prize_5th` - Arrays of other prize numbers
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

## Indexes

- Primary index on `id`
- Unique index on `date`
- Performance index on `date` for lookups

## Prerequisites

- Supabase project configured
- Environment variables set
- Valid API credentials 