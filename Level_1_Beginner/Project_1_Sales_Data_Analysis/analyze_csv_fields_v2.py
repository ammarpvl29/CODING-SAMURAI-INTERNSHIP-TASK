import pandas as pd
import os

# Path to the data directory
data_path = "data/"

# Get all CSV files in the data directory
csv_files = [f for f in os.listdir(data_path) if f.endswith('.csv')]

print("Analysis of CSV Files in data/ directory")
print("=" * 50)

for csv_file in csv_files:
    file_path = os.path.join(data_path, csv_file)
    print(f"\n📁 File: {csv_file}")
    print("-" * 30)
    
    try:
        # Try different encodings for CSV files
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                if encoding != 'utf-8':
                    print(f"Note: Using {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            print(f"Could not read {csv_file} with any standard encoding")
            continue
        
        # Display basic info
        print(f"Shape: {df.shape} (rows, columns)")
        print("\nFields and Data Types:")
        
        # Get field names and data types
        for i, (column, dtype) in enumerate(df.dtypes.items(), 1):
            print(f"{i:2}. {column:25} -> {dtype}")
        
        # Show first few values for context (optional)
        print(f"\nFirst 3 rows preview:")
        print(df.head(3).to_string(index=False))
        
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
    
    print("\n" + "="*50)
