import pandas as pd
import os
import sys

def filter_duplicates(input_file, output_file=None, key_columns=None):
    """
    Filter duplicate entries from a CSV file based on specified key columns.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str, optional): Path to save the filtered CSV file. 
                                    If None, will use input filename with '_filtered' suffix
        key_columns (list, optional): Columns to use for identifying duplicates.
                                     If None, will use ['Name', 'Address', 'Phone']
    
    Returns:
        str: Path to the filtered CSV file
    """
    # Set default key columns if not provided
    if key_columns is None:
        key_columns = ['Name', 'Address', 'Phone']
    
    # Set default output file if not provided
    if output_file is None:
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_filtered{ext}"
    
    # Read the CSV file
    print(f"Reading data from {input_file}...")
    df = pd.read_csv(input_file)
    original_count = len(df)
    
    # Remove duplicates based on key columns
    print(f"Removing duplicates based on columns: {', '.join(key_columns)}...")
    df_filtered = df.drop_duplicates(subset=key_columns, keep='first')
    filtered_count = len(df_filtered)
    
    # Save the filtered data
    df_filtered.to_csv(output_file, index=False)
    
    # Print summary
    removed_count = original_count - filtered_count
    print(f"Original entries: {original_count}")
    print(f"After filtering: {filtered_count}")
    print(f"Removed {removed_count} duplicate entries")
    print(f"Filtered data saved to: {output_file}")
    
    return output_file

if __name__ == "__main__":
    # Check if input file is provided as command line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Find the most recent CSV file in the current directory
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and not f.endswith('_filtered.csv')]
        if not csv_files:
            print("No CSV files found in the current directory.")
            sys.exit(1)
        
        # Sort by modification time (most recent first)
        csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        input_file = csv_files[0]
        print(f"Using most recent CSV file: {input_file}")
    
    # Filter duplicates
    filter_duplicates(input_file) 