import requests
import csv
import time
import os
import concurrent.futures

# API URL
url = "https://lendingapis.finbox.in/v1/masterDashboard/applyNewLoan"

# Load token from an environment variable (safer than hardcoding)
token = os.getenv("FINBOX_API_TOKEN", "kkWjpPsqhZmZfhdiBTilvfGjQBFNSOlIDcIIjrzsFnslPDzJVGVrnFNlbJszgxqw")  # Replace with actual token

# Input & Output CSV files
input_csv_file = "3133042_2025_02_14_500.csv"
output_csv_file = "api_upload_report.csv"

# Number of threads
MAX_THREADS = 10

# Adaptive rate limit variables
failure_count = 0
success_count = 0

# Create a session to reuse TCP connections
session = requests.Session()
session.headers.update({
    "accept": "*/*",
    "accept-language": "en-IN,en-GB;q=0.9,en;q=0.8,en-US;q=0.7",
    "content-type": "application/json",
    "origin": "https://platform.finbox.in",
    "page-header": "Leads Details Page",
    "priority": "u=1, i",
    "referer": "https://platform.finbox.in/",
    "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "token": token,  # Use environment variable for security
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
})

def process_user_id(user_id, max_retries=3, delay=1):
    """Send API request for a given user_id with retries and adaptive rate limiting."""
    global failure_count, success_count

    data = {"userID": user_id}

    for attempt in range(max_retries):
        try:
            response = session.post(url, json=data, timeout=10)
            status_code = response.status_code
            response_text = response.text.strip()

            print(f"UserID: {user_id}, Status: {status_code}, Response: {response_text}")

            if status_code == 200:
                success_count += 1
                return (user_id, status_code, response_text)  # Success
            else:
                print(f"⚠️ Failed attempt {attempt + 1} for UserID {user_id}, retrying...")
                time.sleep(delay * (2 ** attempt))  # Exponential backoff

        except requests.exceptions.RequestException as e:
            print(f"🚨 Network error for UserID {user_id}: {e}, retrying...")
            time.sleep(delay * (2 ** attempt))

    failure_count += 1
    return (user_id, "FAILED", "Max retries exceeded")  # Failure after retries

def adaptive_wait():
    """Slows down execution if too many failures occur."""
    global failure_count, success_count

    total_requests = failure_count + success_count
    if total_requests > 0:
        failure_rate = (failure_count / total_requests) * 100
        if failure_rate > 20:  # If more than 20% of requests are failing, slow down
            print(f"⚠️ High failure rate detected ({failure_rate:.2f}%), pausing for 5 seconds...")
            time.sleep(5)  # Wait 5 seconds before resuming

    # Reset counts periodically
    if total_requests >= 500:
        failure_count, success_count = 0, 0  # Reset counters

def upload_user_ids(input_csv_file, output_csv_file):
    """Reads user IDs from CSV, uploads them using multithreading, and writes results to CSV."""
    user_ids = []

    # Read user IDs from the input CSV
    with open(input_csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Skip header if present
        header = next(reader)
        if not header[0].isdigit():
            print("Skipping header row:", header)
        else:
            file.seek(0)
            reader = csv.reader(file)

        for row in reader:
            if row:
                user_ids.append(row[0])

    # Multithreading using ThreadPoolExecutor
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = list(executor.map(process_user_id, user_ids))

    # Adaptive waiting if API is overloaded
    adaptive_wait()

    # Write results to CSV file
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "status_code", "response_message"])  # Header
        writer.writerows(results)

    # Summary
    success_total = sum(1 for r in results if r[1] == 200)
    print(f"✅ Upload completed! {success_total}/{len(user_ids)} users processed successfully.")
    print(f"📄 Report saved to: {output_csv_file}")

if __name__ == "__main__":
    start_time = time.time()
    upload_user_ids(input_csv_file, output_csv_file)
    print(f"⏳ Total execution time: {time.time() - start_time:.2f} seconds")

