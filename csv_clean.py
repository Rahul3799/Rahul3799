import csv
from datetime import datetime
import re

def is_date(string):
    # Basic date patterns to check
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y", "%d/%m/%y", "%d/%m/%Y"):
        try:
            datetime.strptime(string, fmt)
            return True
        except ValueError:
            continue
    return False

def convert_to_date_format(string):
    # Convert the string to the yyyy-mm-dd format if it is a date
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y", "%d/%m/%y"):
        try:
            date_obj = datetime.strptime(string, fmt)
            return date_obj.strftime('%Y-%m-%d')  # Convert to desired format
        except ValueError:
            continue
    return string  # Return original if not a date

def convert_numeric_to_string(entry):
    try:
        # Try to convert to float, then to int (to drop decimals)
        float_value = float(entry)
        # Check if the value is an integer after conversion
        if float_value.is_integer():
            return str(int(float_value))  # Convert to string without decimals
        else:
            return str(float_value)  # Return as string with decimals if it's not an integer
    except ValueError:
        return str(entry)  # Return original if it fails to convert


def clean_entry(entry):
    """Clean an individual CSV entry."""
    # Remove leading/trailing whitespaces and Excel-specific characters
    cleaned = entry.strip()
    cleaned = cleaned.replace("\u00A0", " ")  # Replace non-breaking spaces
    cleaned = cleaned.replace("\r", "").replace("\n", "")  # Remove carriage returns and newlines
    cleaned = re.sub(r"[\u200B\uFEFF]", "", cleaned)
    # Replace multiple spaces with a single space
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned

def validate_pan(pan):
    pan_regex = r"^[A-Z]{5}[0-9]{4}[A-Z]$"
    if re.match(pan_regex, pan):
        return True
    else:
        return False

def convert_csv_to_text(input_file, output_file):
    with open(input_file, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        data = []
        i = 1
        for row in reader:
            print(i)
            i += 1
            string_row = []
            for z, entry in enumerate(row):
               
            
                entry = clean_entry(entry)
                if z== 0 and i > 2:
                    entry = entry.upper()
                    if not validate_pan(entry):
                        print("pan: ",i, entry, validate_pan(entry))
                if is_date(entry):
                    # Convert to yyyy-mm-dd if it's a date
                    formatted_date = convert_to_date_format(entry)
                    string_row.append(formatted_date)
                else:
                    # Convert numeric types to strings without decimals
                    string_row.append(convert_numeric_to_string(entry))
            data.append(string_row)

    # Write the converted data to a new CSV file
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)


# Example usage
input_csv_file = "Bandhan_PA_5K_Base 3_Finbox_12022025.csv"  # Replace with your input file name
output_csv_file = '/Users/abhishekkar/Downloads/13_Feb_cleaned.csv'  # Replace with your desired output file name
convert_csv_to_text(input_csv_file, output_csv_file)

print(f"Converted CSV saved to {output_csv_file}")


