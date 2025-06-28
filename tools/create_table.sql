-- Create lottery_draws table for lottery data storage
-- Run this in your Supabase SQL Editor

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

-- Create index on date for faster lookups
CREATE INDEX IF NOT EXISTS idx_lottery_draws_date ON lottery_draws(date);

-- Verify table was created
SELECT 'Table created successfully!' as status; 