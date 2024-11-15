#!/usr/bin/env python3

"""
Script to create a metadata file for fine-tuning datasets.

This script processes a directory of HRRR files (.grib2) and corresponding caption files (.csv),
and generates a single metadata file in CSV format.

Usage:
    python create_metadata.py --image_dir <IMAGE_DIR> --caption_dir <CAPTION_DIR> --output_file <OUTPUT_FILE>

Example:
    python create_metadata.py --image_dir hrrr --caption_dir csv_reports --output_file metadata.csv
"""

import os
import pandas as pd
import argparse


def create_metadata_file(image_dir, caption_dir, output_file):
    """
    Create a metadata CSV file by matching HRRR images with their captions.

    Args:
        image_dir (str): Path to the directory containing HRRR image files (.grib2).
        caption_dir (str): Path to the directory containing caption files (.csv).
        output_file (str): Path to save the generated metadata CSV file.

    Returns:
        None
    """
    metadata_rows = []

    # Verify directories exist
    if not os.path.isdir(image_dir):
        raise FileNotFoundError(f"Image directory not found: {image_dir}")
    if not os.path.isdir(caption_dir):
        raise FileNotFoundError(f"Caption directory not found: {caption_dir}")

    # Process each image file
    for filename in os.listdir(image_dir):
        if filename.endswith(".grib2"):
            # Generate the corresponding caption file name
            label_filename = f"{filename.split('.')[1]}.csv"
            label_path = os.path.join(caption_dir, label_filename)

            # Check if caption file exists
            if not os.path.isfile(label_path):
                continue

            try:
                # Read the caption file
                caption_df = pd.read_csv(label_path, index_col=0)
                caption = caption_df.iloc[0]["discussion"].strip()

                # Save metadata
                metadata_rows.append({"file_name": filename, "text": caption})
            except Exception as e:
                raise ValueError(f"Error processing caption file {label_path}: {e}")

    # Write metadata to output file
    if metadata_rows:
        metadata_df = pd.DataFrame(metadata_rows)
        metadata_df.to_csv(output_file, index=False)
    else:
        raise ValueError("No metadata was generated. Please check input files and directories.")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Create a metadata file for fine-tuning datasets.")
    parser.add_argument("--image_dir", required=True, help="Directory containing HRRR image files (.grib2).")
    parser.add_argument("--caption_dir", required=True, help="Directory containing caption files (.csv).")
    parser.add_argument("--output_file", required=True, help="Path to save the output metadata CSV file.")
    args = parser.parse_args()

    # Call the metadata creation function
    create_metadata_file(args.image_dir, args.caption_dir, args.output_file)
