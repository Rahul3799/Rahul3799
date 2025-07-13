import csv

def generate_sql_from_csv(input_csv, output_sql):
    with open(input_csv, mode='r', encoding='utf-8') as infile, open(output_sql, mode='w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        
        values_list = []
        for row in reader:
            lender_id = '66605390-47c9-47e3-ba71-ab5dc79e8477'
            list_id = '050c2d09-363e-48eb-98b3-5e2c7e282dd8'
            pincode = row.get("pincode", "")
            
            values_list.append(f"('{lender_id}', '{list_id}', '{pincode}', NOW())")
        
        if values_list:
            query = "INSERT INTO serviceable_pincodes (lender_id, list_id, pincode, created_at) VALUES \n"
            query += ",\n".join(values_list) + ";"
            outfile.write(query)
            print("SQL file has been generated successfully!")

# Example usage
generate_sql_from_csv('3rdFeb2025.csv', 'kisst_pincode_update.sql')
