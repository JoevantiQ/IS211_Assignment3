import argparse
import requests
import csv
from io import StringIO


def process_data(data):
    """Processes CSV project data and prints key insights."""
    reader = csv.DictReader(StringIO(data))
    projects = list(reader)

    print(f"Total projects: {len(projects)}")

    # Example: Count projects by status
    status_count = {}
    for project in projects:
        status = project.get("Status", "Unknown")
        status_count[status] = status_count.get(status, 0) + 1

    print("Project status breakdown:")
    for status, count in status_count.items():
        print(f"  {status}: {count}")


def main(url="http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"):
    """Fetches data from a given URL and processes it."""
    print(f"Fetching data from {url}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        process_data(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str,
                        default="http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv")
    args = parser.parse_args()
    main(args.url)

