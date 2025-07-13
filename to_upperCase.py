import csv

# Specify the input and output CSV file paths
input_csv_file = 'Book2.csv'
output_csv_file = 'Uppercase.csv'

# Open the input CSV file for reading and the output CSV file for writing
with open(input_csv_file, 'r') as infile, open(output_csv_file, 'w', newline='') as outfile:
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)
    
    # Process each row
    for row in csv_reader:
        # Convert all values in the row to uppercase
        updated_row = [value.upper() for value in row]
        csv_writer.writerow(updated_row)

print(f"Updated CSV saved as '{output_csv_file}'")
