#!/usr/bin/env python3

"""
Script to scrape textual weather forecast reports from SPC (Storm Prediction Center).

This script fetches weather reports within a specified date range and extracts summary 
discussions from the reports. The extracted data is saved as CSV files.

Usage:
    python weather_report_data_scraping.py --start_date "YYYY-MM-DD" --end_date "YYYY-MM-DD"

Example:
    python weather_report_data_scraping.py --start_date "2021-06-27" --end_date "2021-06-27"
"""

import argparse
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_weather_reports(start_date, end_date, output_path="./csv_reports/"):
    """
    Scrape weather forecast reports from SPC and save them as CSV files.

    Args:
        start_date (str): Start date of the time range in YYYY-MM-DD format.
        end_date (str): End date of the time range in YYYY-MM-DD format.
        output_path (str): Directory to save the output CSV files.

    Returns:
        None
    """
    # Construct the SPC URL for the specified date range
    url = f"https://www.spc.noaa.gov/cgi-bin-spc/getacrange-aws.pl?date0={start_date}&date1={end_date}"
    print("Base URL:", url)

    # Fetch the page content
    page = requests.get(url)
    try:
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as e:
        raise Exception(f"Error parsing HTML content: {e}")

    # Extract report links from the page
    links = soup.find_all('a', href=True)
    report_links = [
        f"https://spc.noaa.gov{a['href']}"
        for a in links
        if "otlk" in a["href"] and ".html" in a["href"]
    ]
    print("URLs to scrape:", report_links)

    # Initialize a dictionary to store the scraped data
    outlook_data = {
        "date": [],
        "time": [],
        "url": [],
        "discussion": [],
    }

    # Scrape each report
    for report_url in report_links:
        date = report_url.split(".")[-2].split("_")[-2]
        time = report_url.split(".")[-2].split("_")[-1]

        try:
            report_page = requests.get(report_url)
            soup = BeautifulSoup(report_page.content, "html.parser")
            pre_tags = soup.find_all('pre')

            for pre_tag in pre_tags:
                # Extract the "summary" section from the report
                text_report = pre_tag.text
                summary = text_report.split("...SUMMARY...")[-1].split("...")[0]

                outlook_data["date"].append(date)
                outlook_data["time"].append(time)
                outlook_data["url"].append(report_url)
                outlook_data["discussion"].append(summary)

        except Exception as e:
            print(f"Error processing URL {report_url}: {e}")
            continue

    # Save the scraped data as a CSV file
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file = os.path.join(output_path, f"{date}.csv")
    df = pd.DataFrame(outlook_data)
    df.to_csv(output_file, index=False)
    print(f"Data saved to: {output_file}")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Scrape weather forecast reports from SPC.")
    parser.add_argument("--start_date", type=str, required=True, help="Start date of the time range (YYYY-MM-DD).")
    parser.add_argument("--end_date", type=str, required=True, help="End date of the time range (YYYY-MM-DD).")
    args = parser.parse_args()

    # Call the main function
    fetch_weather_reports(args.start_date, args.end_date)
