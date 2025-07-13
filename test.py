import pandas as pd
import json

# File names
input_file = "pan_user_name.xlsx"
output_file = "pan_user_name_output.xlsx"

# Read Excel file into DataFrame
df = pd.read_excel(input_file)

def extract_branch_code(json_str):
    try:
        data = json.loads(json_str)
        return data.get("sourcingBranchCode", None)
    except (json.JSONDecodeError, TypeError):
        return None

# Apply extraction to partner_data column
df["sourcing_branch_code"] = df["partner_data"].apply(extract_branch_code)

# Write output to new Excel file
df.to_excel(output_file, index=False)

print("Processing complete! Data saved to", output_file)
