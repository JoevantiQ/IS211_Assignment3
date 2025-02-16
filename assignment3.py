import argparse
import requests
import csv
import re
from collections import Counter
from io import StringIO


def download_file(url):
    """Downloads a file from the given URL and returns its content as a string."""
    response = requests.get(url)
    return response.text

def process_log_file(log_content):
    """Processes the log file and extracts relevant data."""
    image_pattern = re.compile(r'.*\.(jpg|gif|png)$', re.IGNORECASE)
    browser_pattern = re.compile(r'(Firefox|Chrome|Safari|MSIE)', re.IGNORECASE)

    total_requests = 0
    image_requests = 0
    browser_counts = Counter()

    csv_reader = csv.reader(StringIO(log_content))

    for row in csv_reader:
        if len(row) < 5:
            continue  # Skip rows that do not have 5 columns

        path, _, user_agent, _, _ = row
        total_requests += 1

        # Count image requests
        if image_pattern.match(path):
            image_requests += 1

        # Determine browser type
        match = browser_pattern.search(user_agent)
        if match:
            browser_counts[match.group(1)] += 1

    # Calculate image request percentage
    image_percentage = (image_requests / total_requests) * 100 \
        if total_requests \
        else 0

    # Find the most popular browser
    most_popular_browser = browser_counts.most_common(1)
    popular_browser = most_popular_browser[0][0] \
        if most_popular_browser \
        else "Unknown"

    return image_requests, image_percentage, popular_browser


def main(url="http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"):
    """Main function to download, process, and analyze the web log file."""
    print(f"Running main with URL = {url}...")

    # Download and process the log file
    log_content = download_file(url)
    image_requests, image_percentage, popular_browser = process_log_file(log_content)

    # Print results
    print(f"Image requests account for {image_percentage:.2f}% of all requests.")
    print(f"The most popular browser is {popular_browser}.")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        help="URL to the datafile",
        type=str,
        default="http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"
    )
    args = parser.parse_args()
    main(args.url)
