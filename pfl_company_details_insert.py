import csv

def generate_insert_queries(input_csv, output_csv):
    with open(input_csv, mode='r', encoding='utf-8') as infile, open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read the header row (assuming the first row contains column names)
        headers = next(reader)
        
        queries = []
        for row in reader:
            company_code = ''
            company_name = row[0]
            source_entity_id = 'e023bd9e-46e2-4964-a8e7-d3e73e62421c'
            company_category = row[2]
            company_domain = row[1].split(';')  # Assuming multiple domains are separated by semicolons
            company_metadata = 'PRIME'
            
            company_domain_array = ', '.join([f"'{domain.strip()}'" for domain in company_domain])
            query = f"INSERT INTO company_details (company_code, company_name, created_at, source_entity_id, company_category, company_domain, company_metadata) VALUES ('{company_code}', '{company_name}', NOW(), '{source_entity_id}', '{company_category}', ARRAY[{company_domain_array}], '{{\"segment\": \"{company_metadata}\"}}');"

            queries.append([query])
        
        # Write queries to output CSV
        writer.writerows(queries)
        print("SQL queries have been written to", output_csv)

# Example usage
generate_insert_queries('Master_List11Feb25.csv', 'Master_List11Feb25_output.csv')