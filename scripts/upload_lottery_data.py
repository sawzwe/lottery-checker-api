#!/usr/bin/env python3
"""
Simple script to upload lottery CSV data to Supabase
Usage: python upload_lottery_data.py [csv_file_path]
"""

import sys
from lottery_uploader import LotteryUploader

def main():
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = input("Enter the path to your CSV file: ").strip()
    
    if not csv_file:
        print("No file path provided. Exiting.")
        return
    
    try:
        uploader = LotteryUploader()
        print("🎲 Lottery Data Uploader Starting...")
        print("="*50)
        
        # Display table creation instructions
        print("📋 First time setup:")
        print("Make sure you've created the database table in Supabase.")
        print("If not, run the SQL from the README.md file in your Supabase SQL editor.")
        print("="*50)
        
        # Start upload
        success = uploader.upload_csv(csv_file)
        
        if success:
            print("\n🎉 Upload process completed successfully!")
            print("✅ All data has been verified in the database.")
        else:
            print("\n❌ Upload process completed with errors!")
            print("⚠️  Some data may not have been uploaded. Check the log above.")
            sys.exit(1)
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        if "does not exist" in str(e):
            print("\n🔧 To fix this:")
            print("1. Go to your Supabase dashboard")
            print("2. Open the SQL Editor")
            print("3. Run the table creation SQL from the README.md")
        sys.exit(1)

if __name__ == "__main__":
    main() 