import csv
import os
import re
from datetime import datetime
import time
import pandas as pd
import requests
from token_generator import get_token

# Header mapping
header_map = {
    "pan": "Pan Card",
    "roi": "ROI",
    "tenure": "Tenure",
    "expected_loan_amount": "Expected Loan Amount",
    "processing_fee": "Processing fee",
    "partner_code": "Partner code",
    "product_type": "Product type",
    "processing_fee_type": "Processing Fee Type",
    "mobilenumber": "Mobile",
    "mobile_no": "Mobile",
    "expiry_at": "Expiry At",
    "firstname": "firstName",
    "middlename": "middleName",
    "lastname": "lastName",
    # "dob": "dob",
    # "occupation": "occupation",
    # "gender": "gender",
    "currentaddressline1": "currentAddressLine1",
    "currentaddressline2": "currentAddressLine2",
    "land_mark": "currentAddressLandMark",
    "currentaddresspincode": "currentAddressPincode",
    "currentaddresscity": "currentAddressCity",
    "currentaddressstate": "currentAddressState",
    "typeofbusiness": "typeOfBusiness",
    "natureofbusiness": "natureOfBusiness",
    # "industry": "industry",
    # "subindustry": "subindustry",
    "businessname": "businessName",
    "dateofincorporation": "dateOfIncorporation",
    "businessaddressline1": "businessAddressLine1",
    "businessaddressline2": "businessAddressLine2",
    "businessaddresslandmark": "businessAddressLandmark",
    "businessaddresspincode": "businessAddressPincode",
    "businessaddressstate": "businessAddressState",
    "businessaddresscity": "businessAddressCity",
    "repaymentbankname": "repaymentBankName",
    "repaymentbankaccountnumber": "repaymentBankAccountNumber",
    "repaymentifsccode": "repaymentIFSCCode",
    "repaymentaccounttype": "repaymentAccountType",
    "udyamnumber": "udyamNumber",
    "ucic": "ucidID",
    "maxamount": "maxAmount",
    "minamount": "minAmount",
    "mintenure": "minTenure",
    "maxtenure": "maxTenure",
    "maxemi": "maxEMI",
    # "email": "email",
    "customer_cif": "ccid",
    "customer_cid_id": "ccid",
    "InstallmentProgramme": "installmentProgramme",
    "cust_brn_code": "sourcingBranchCode"
}


# === Cleaning and Utility Functions ===
def is_date(string):
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y", "%d/%m/%y"):
        try:
            datetime.strptime(string, fmt)
            return True
        except:
            continue
    return False

def convert_to_date_format(string):
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(string, fmt).strftime('%Y-%m-%d')
        except:
            continue
    return string

def convert_numeric_to_string(entry):
    try:
        f = float(entry)
        return str(int(f)) if f.is_integer() else str(f)
    except:
        return str(entry)

def clean_email(email):
    return re.sub(r"[\\\/,'\":;]", "", email)

def clean_address(entry):
    entry = re.sub(r"['\t@]", "", entry)
    entry = re.sub(r'"', " ", entry)
    entry = re.sub(r"[\n]", " ", entry)
    entry = re.sub(r"\\", "/", entry)
    entry = re.sub(r";", " ", entry)
    entry = re.sub(r"\\N", " ", entry)
    return re.sub(r"\s+", " ", entry).strip()

def clean_entry(entry, column_name):
    cleaned = str(entry).strip()
    cleaned = re.sub(r"[\u00A0\u200B\uFEFF\r\n]+", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)

    if column_name == "email":
        return clean_email(cleaned)
    elif column_name in [
        "currentAddressLine1", "currentAddressLine2", "currentAddressLandMark",
        "currentAddressCity", "businessAddressLine1", "businessAddressLine2",
        "businessAddressLandmark", "businessAddressCity"
    ]:
        return clean_address(cleaned)

    return cleaned

def write_chunks_to_csv(data, base_output_file, chunk_size=50000):
    header = data[0]
    rows = data[1:]
    base_name, ext = os.path.splitext(base_output_file)
    total = len(rows)
    parts = (total // chunk_size) + (1 if total % chunk_size else 0)
    chunk_files = []

    for i in range(parts):
        chunk = rows[i * chunk_size:(i + 1) * chunk_size]
        file_path = f"{base_name}_part{i+1}.csv"
        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(chunk)
        chunk_files.append(file_path)
        print(f"✅ Saved chunk {i+1} to {file_path}")

    return chunk_files

def read_input_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        return pd.read_csv(file_path, dtype=str, keep_default_na=False)
    elif ext == '.xlsx':
        return pd.read_excel(file_path, dtype=str, keep_default_na=False, engine='openpyxl')
    elif ext == '.xlsb':
        return pd.read_excel(file_path, dtype=str, keep_default_na=False, engine='pyxlsb')
    else:
        raise ValueError("Unsupported file type. Use .csv, .xlsx, or .xlsb")

# === File Processing and Upload ===
def convert_file(input_file, output_file, chunk_size=50000):
    df = read_input_file(input_file)

    if df.columns[0].lower().strip().replace('.', '') in ['sno', 'slno', 'sl no']:
        df.drop(df.columns[0], axis=1, inplace=True)

    new_columns = []
    seen_pan = False

    for col in df.columns:
        col_clean = col.lower().strip()
        if col_clean == 'pan' and not seen_pan:
            new_columns.append('Pan Card')
            seen_pan = True
        elif col_clean.startswith('pan.') or (col_clean == 'pan' and seen_pan):
            new_columns.append('pan')
        else:
            new_columns.append(header_map.get(col_clean, col))

    df.columns = new_columns
    df["sourcingChannelCode"] = "BRANCH"

    data = [df.columns.tolist()]
    total_rows = len(df)

    for idx, (_, row) in enumerate(df.iterrows(), start=1):
        row_dict = {}
        for col_name, entry in row.items():
            entry = clean_entry(entry, col_name)
            entry = convert_to_date_format(entry) if is_date(entry) else convert_numeric_to_string(entry)

            if col_name == "maxEMI":
                try:
                    entry = str(int(round(float(entry))))
                except:
                    pass

            if col_name in ['Pan Card', 'pan']:
                entry = entry.upper()

            row_dict[col_name] = entry

        ucid = row_dict.get("ucidID", "").strip()
        ccid = row_dict.get("ccid", "").strip()

        if ucid and not ccid:
            row_dict["ccid"] = ucid
            row_dict["ucidID"] = ""
        elif ucid and ccid:
            row_dict["ccid"], row_dict["ucidID"] = ucid, ccid

        max_amt = row_dict.get("maxAmount", "").strip()
        min_amt = row_dict.get("minAmount", "").strip()

        try:
            if max_amt and min_amt and float(max_amt) < float(min_amt):
                print(f"⚠️  Invalid amount at row {idx + 1}: maxAmount {max_amt} < minAmount {min_amt}")
        except ValueError:
            print(f"⚠️  Non-numeric values at row {idx + 1}: maxAmount={max_amt}, minAmount={min_amt}")

        cleaned_row = [row_dict.get(col, "") for col in df.columns]
        data.append(cleaned_row)

        if idx % max(1, total_rows // 100) == 0 or idx == total_rows:
            percent_complete = (idx / total_rows) * 100
            print(f"Progress: {percent_complete:.0f}%")

    return write_chunks_to_csv(data, output_file, chunk_size)

def upload_csv_file(token, file_path):
    url = 'https://lendingapis.finbox.in/v1/lender/preApproveCustomers'
    headers = {
        'page-header': 'Settings Page',
        'token': token
    }

    with open(file_path, 'rb') as file_data:
        files = {'file': (os.path.basename(file_path), file_data)}
        response = requests.post(url, headers=headers, files=files)

    print(f"\n📦 Uploaded: {file_path}")
    print(f"✅ Status Code: {response.status_code}")
    print("🔁 Response:", response.text)

# === Main Runner ===
if __name__ == "__main__":
    remote_file_name = input("📝 Enter the exact file name on server (e.g., myfile.xlsx): ").strip()
    download_path = "/Users/abhishekkar/Downloads"
    local_file_path = os.path.join(download_path, os.path.basename(remote_file_name))

    # SCP Download Command
    scp_cmd = f'scp -i /Users/abhishekkar/Downloads/MFL_BL_keys/MFL_BL_sftp_user.pem ' \
              f'MFL_BL_sftp_user@s-0ca543ee379a4fa4b.server.transfer.ap-south-1.amazonaws.com:"{remote_file_name}" "{local_file_path}"'

    print("📥 Downloading file via SCP...")
    result = os.system(scp_cmd)

    if result != 0:
        print("❌ Failed to download file. Please check the file name or your network connection.")
        exit(1)

    print(f"✅ Downloaded file to: {local_file_path}")
    
    # Step 2: Clean and chunk
    output_path = os.path.splitext(local_file_path)[0] + "_cleaned.csv"
    print("🔄 Processing and cleaning file...")
    chunk_files = convert_file(local_file_path, output_path)
    print("✅ File cleaned and split into chunks.")

    print("\n🗃️ Chunked Files:")
    for f in chunk_files:
        print(" -", f)

    confirm = input(f"\n🚀 Do you want to upload all {len(chunk_files)} parts? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y']:
        print("🔐 Getting token...")
        token = get_token("lender")
        if token:
            for idx, f in enumerate(chunk_files, start=1):
                print(f"\n📤 Uploading chunk {idx}/{len(chunk_files)}...")
                upload_csv_file(token, f)
                if idx < len(chunk_files):
                    print("⏳ Waiting 5 seconds before next upload...")
                    time.sleep(5)
        else:
            print("❌ Failed to get token.")
    else:
        print("⏹️ Upload cancelled by user.")
