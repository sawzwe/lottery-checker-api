#!/usr/bin/env python3
"""
Script to create the lottery_draws table in Supabase database
"""

import os
from dotenv import load_dotenv
from config.config import get_supabase_config
from supabase import create_client

# Load environment variables
load_dotenv()

def create_lottery_table():
    """Create the lottery_draws table with proper schema"""
    
    try:
        print("🔗 Connecting to Supabase...")
        url, key = get_supabase_config()
        supabase = create_client(url, key)
        
        # SQL to create the table
        create_table_sql = """
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
        """
        
        # Create index for faster date lookups
        create_index_sql = """
        CREATE INDEX IF NOT EXISTS idx_lottery_draws_date ON lottery_draws(date);
        """
        
        print("📋 Creating lottery_draws table...")
        
        # Execute table creation
        result1 = supabase.rpc('exec_sql', {'sql': create_table_sql}).execute()
        print("✅ Table created successfully!")
        
        # Execute index creation  
        result2 = supabase.rpc('exec_sql', {'sql': create_index_sql}).execute()
        print("✅ Index created successfully!")
        
        # Verify table exists
        print("🔍 Verifying table creation...")
        test_result = supabase.table('lottery_draws').select('count').execute()
        print("✅ Table verification successful!")
        
        print("\n🎉 Database setup complete!")
        print("You can now upload lottery data using:")
        print("python upload_lottery_data.py your_file.csv")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        
        if "does not exist" in error_msg and "exec_sql" in error_msg:
            print("\n⚠️  Direct SQL execution not available.")
            print("Please create the table manually in Supabase:")
            print("\n1. Go to your Supabase dashboard")
            print("2. Open SQL Editor")
            print("3. Run this SQL:")
            print("\n" + "="*50)
            print(create_table_sql)
            print(create_index_sql)
            print("="*50)
            return False
        else:
            print(f"❌ Error creating table: {e}")
            return False

def main():
    print("🎲 Lottery Database Setup")
    print("="*50)
    
    try:
        success = create_lottery_table()
        if not success:
            print("\n📝 Manual Setup Required:")
            print("Since automatic table creation failed, please:")
            print("1. Copy the SQL commands shown above")
            print("2. Go to your Supabase dashboard → SQL Editor")
            print("3. Paste and run the SQL")
            print("4. Then run: python upload_lottery_data.py")
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\n🔧 Manual Setup Instructions:")
        print("1. Go to your Supabase dashboard")
        print("2. Open SQL Editor")
        print("3. Copy and run the SQL from README.md")

if __name__ == "__main__":
    main() 