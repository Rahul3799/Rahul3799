import os
import time
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

# Folder to store downloaded PDFs
DOWNLOAD_FOLDER = "downloaded_pdfs"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Load the Excel file
file_path = "3172671_2025_02_18.xlsx"  # Change this to your actual file path
df = pd.read_excel(file_path, engine="openpyxl")  # Ensure openpyxl is installed

# Function to download a single file with retries
def download_pdf(row):
    loan_no = str(row["loan_application_no"]).strip()
    uan = str(row["uan"]).strip()
    pdf_url = str(row["pdf_url"]).strip()

    if pd.notna(loan_no) and pd.notna(uan) and pd.notna(pdf_url):
        file_name = f"{loan_no}_{uan}.pdf"
        file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

        retries = 3  # Number of retries
        for attempt in range(retries):
            try:
                # Download the file
                response = requests.get(pdf_url, stream=True, timeout=10)
                response.raise_for_status()  # Raise an error for bad responses

                # Save the file
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)

                print(f"Downloaded: {file_name}")
                return  # Exit the function if download is successful

            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed for {pdf_url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2)  # Wait for 2 seconds before retrying

        print(f"Failed to download after {retries} attempts: {pdf_url}")

# Using ThreadPoolExecutor for multithreading
MAX_THREADS = 2  # Adjust the number of threads as needed

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    executor.map(download_pdf, df.to_dict(orient="records"))

print("Download process completed.")
