import os
import csv
import ast
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from config.config import get_supabase_config

# Load environment variables
load_dotenv()

class LotteryUploader:
    def __init__(self):
        """Initialize the Supabase client"""
        try:
            self.supabase_url, self.supabase_key = get_supabase_config()
        except ValueError as e:
            print(f"Configuration Error: {e}")
            raise
        
        try:
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        except TypeError as e:
            # Handle version compatibility issues
            if "proxy" in str(e):
                print("⚠️  Detected Supabase client version issue, trying alternative initialization...")
                # Try without any optional parameters that might cause issues
                self.supabase = create_client(self.supabase_url, self.supabase_key)
            else:
                raise
        
    def parse_array_field(self, field_value):
        """Parse string representation of Python list into actual list"""
        try:
            if isinstance(field_value, str) and field_value.startswith('['):
                # Use ast.literal_eval to safely evaluate the string as a Python literal
                return ast.literal_eval(field_value)
            elif isinstance(field_value, list):
                return field_value
            else:
                return []
        except (ValueError, SyntaxError):
            print(f"Error parsing array field: {field_value}")
            return []
    
    def check_existing_record(self, date_str):
        """Check if a record with the given date already exists"""
        try:
            result = self.supabase.table('lottery_draws').select('date').eq('date', date_str).execute()
            return len(result.data) > 0
        except Exception as e:
            error_msg = str(e)
            if 'does not exist' in error_msg:
                print(f"⚠️  Table 'lottery_draws' does not exist. Please create it first!")
                print("Run the SQL from the README in your Supabase SQL editor.")
                raise Exception("Database table 'lottery_draws' not found. Please create the table first.")
            else:
                print(f"Error checking existing record for date {date_str}: {e}")
                raise
    
    def prepare_record(self, row):
        """Prepare a single CSV row for database insertion"""
        
        # Handle prize_2digits - could be string or int
        prize_2digits = row['prize_2digits']
        if isinstance(prize_2digits, str):
            prize_2digits = int(prize_2digits) if prize_2digits.isdigit() else None
        elif isinstance(prize_2digits, (int, float)):
            prize_2digits = int(prize_2digits)
        else:
            prize_2digits = None
            
        record = {
            'date': row['date'],
            'prize_1st': str(row['prize_1st']),
            'prize_pre_3digit': self.parse_array_field(row['prize_pre_3digit']),
            'prize_sub_3digits': self.parse_array_field(row['prize_sub_3digits']),
            'prize_2digits': prize_2digits,
            'nearby_1st': self.parse_array_field(row['nearby_1st']),
            'prize_2nd': self.parse_array_field(row['prize_2nd']),
            'prize_3rd': self.parse_array_field(row['prize_3rd']),
            'prize_4th': self.parse_array_field(row['prize_4th']),
            'prize_5th': self.parse_array_field(row['prize_5th'])
        }
        return record
    
    def upload_csv(self, csv_file_path):
        """Upload lottery data from CSV file to Supabase"""
        if not os.path.exists(csv_file_path):
            print(f"Error: CSV file '{csv_file_path}' not found")
            return
        
        print(f"Starting upload from {csv_file_path}")
        
        uploaded_count = 0
        skipped_count = 0
        error_count = 0
        
        try:
            # Read CSV file
            df = pd.read_csv(csv_file_path)
            
            print(f"Found {len(df)} records in CSV file")
            
            for index, row in df.iterrows():
                try:
                    date_str = row['date']
                    
                    # Check if record already exists
                    if self.check_existing_record(date_str):
                        print(f"Record for {date_str} already exists, skipping...")
                        skipped_count += 1
                        continue
                    
                    # Prepare record for insertion
                    record = self.prepare_record(row)
                    
                    # Insert into Supabase
                    result = self.supabase.table('lottery_draws').insert(record).execute()
                    
                    if result.data and len(result.data) > 0:
                        # Verify the record was actually inserted by checking it exists
                        verification = self.supabase.table('lottery_draws').select('date').eq('date', date_str).execute()
                        if verification.data and len(verification.data) > 0:
                            print(f"✓ Successfully uploaded and verified record for {date_str}")
                            uploaded_count += 1
                        else:
                            print(f"✗ Upload appeared successful but verification failed for {date_str}")
                            error_count += 1
                    else:
                        print(f"✗ Failed to upload record for {date_str} - no data returned")
                        error_count += 1
                        
                except Exception as e:
                    print(f"✗ Error processing record {index + 1}: {e}")
                    error_count += 1
                    continue
        
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return
        
        # Summary
        print(f"\n=== Upload Summary ===")
        print(f"Total records processed: {len(df)}")
        print(f"Successfully uploaded: {uploaded_count}")
        print(f"Skipped (already exists): {skipped_count}")
        print(f"Errors: {error_count}")
        
        # Return success status - only true if no errors occurred
        success = error_count == 0
        if not success:
            print(f"\n⚠️  Upload completed with {error_count} errors!")
            print("❌ Data integrity compromised - some records were not uploaded.")
        
        return success
        
    def create_table_if_not_exists(self):
        """Create the lottery_draws table if it doesn't exist (you'll need to run this SQL in Supabase)"""
        sql = """
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
        """
        print("Please run the following SQL in your Supabase SQL editor:")
        print(sql)

def main():
    """Main function to run the uploader"""
    uploader = LotteryUploader()
    
    # Print table creation SQL (run this manually in Supabase first)
    print("First, make sure your table exists in Supabase:")
    uploader.create_table_if_not_exists()
    print("\n" + "="*50 + "\n")
    
    # Get CSV file path from user
    csv_file = input("Enter the path to your CSV file: ").strip()
    
    if not csv_file:
        print("No file path provided. Exiting.")
        return
    
    # Start upload
    uploader.upload_csv(csv_file)

if __name__ == "__main__":
    main() 