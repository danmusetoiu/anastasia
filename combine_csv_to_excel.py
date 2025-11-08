#!/usr/bin/env python3
"""
Script to combine multiple CSV files into a single Excel file.
Each CSV's columns will be prefixed with the file's label.
"""

import pandas as pd
import glob
import os
from pathlib import Path

def read_csv_file(filepath):
    """
    Read a CSV file and return a DataFrame with proper column names.
    The CSV format has:
    - Line 1: Label/name
    - Line 2: Column headers
    - Lines 3+: Data (until empty line or metadata starts)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Get the label from the filename (without extension)
    label = Path(filepath).stem

    # Find where the actual data ends (before metadata)
    data_lines = []
    for i, line in enumerate(lines[2:], start=2):  # Skip first 2 lines
        line = line.strip()
        # Stop if we hit an empty line or non-numeric data
        if not line or (line and not any(c.isdigit() for c in line.split(',')[0])):
            break
        data_lines.append(line)

    # Read the headers from line 2
    headers_line = lines[1].strip()
    headers = [h.strip() for h in headers_line.split(',') if h.strip()]

    # Parse data lines
    data = []
    for line in data_lines:
        values = [v.strip() for v in line.split(',')]
        # Only take as many values as we have headers
        data.append(values[:len(headers)])

    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Convert numeric columns
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    # Prefix column names with the label
    df.columns = [f"{label}_{col}" for col in df.columns]

    return df, label

def combine_csv_files(output_filename='combined_data.xlsx'):
    """
    Combine all CSV files in the current directory into a single Excel file.
    """
    # Get all CSV files
    csv_files = sorted(glob.glob('*.csv'))

    if not csv_files:
        print("No CSV files found!")
        return

    print(f"Found {len(csv_files)} CSV files:")
    for f in csv_files:
        print(f"  - {f}")

    # Read all CSV files
    all_dataframes = []
    labels = []

    for csv_file in csv_files:
        try:
            df, label = read_csv_file(csv_file)
            all_dataframes.append(df)
            labels.append(label)
            print(f"✓ Processed {csv_file}: {len(df)} rows, {len(df.columns)} columns")
        except Exception as e:
            print(f"✗ Error processing {csv_file}: {e}")

    if not all_dataframes:
        print("No data to combine!")
        return

    # Combine all dataframes horizontally (side by side)
    combined_df = pd.concat(all_dataframes, axis=1)

    print(f"\nCombined DataFrame: {len(combined_df)} rows, {len(combined_df.columns)} columns")

    # Write to Excel
    combined_df.to_excel(output_filename, index=False, sheet_name='Combined Data')

    print(f"\n✓ Successfully created {output_filename}")
    print(f"  Total rows: {len(combined_df)}")
    print(f"  Total columns: {len(combined_df.columns)}")
    print(f"  Files combined: {len(all_dataframes)}")

if __name__ == '__main__':
    combine_csv_files()
