import os
import pandas as pd

# Load the CSV file containing the mapping
csv_file = "81 cases agreement_loan_number mapping.csv"  # Update with your actual CSV filename
df = pd.read_csv(csv_file)

# Convert mapping to a dictionary for fast lookup
id_to_no_mapping = dict(zip(df["loan_application_id"], df["loan_application_no"]))

# Folder where PDF files are stored
pdf_folder = "/Users/abhishekkar/Downloads/sakshi_files"  # Update this with your actual folder path

# Loop through all files in the folder
for filename in os.listdir(pdf_folder):
    if filename.startswith("signed_agreement_") and filename.endswith(".pdf"):
        # Extract loan_application_id from the filename
        loan_id = filename.replace("signed_agreement_", "").replace(".pdf", "")

        # Check if the loan_id exists in the mapping
        if loan_id in id_to_no_mapping:
            new_filename = f"signed_agreement_{id_to_no_mapping[loan_id]}.pdf"
            old_path = os.path.join(pdf_folder, filename)
            new_path = os.path.join(pdf_folder, new_filename)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} ➝ {new_filename}")
        else:
            print(f"Skipping: {filename} (No matching loan_application_no found)")

print("File renaming completed!")
