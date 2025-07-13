import pandas as pd

def generate_sql_from_csv(file_path):
    # Load CSV file
    df = pd.read_csv(file_path)
    
    # Ensure required columns exist
    if 'user_id' not in df.columns or 'partner_data' not in df.columns:
        raise ValueError("CSV file must contain 'user_id' and 'partner_data' columns")
    
    # Generate SQL statements
    sql_statements = []
    for _, row in df.iterrows():
        user_id = row['user_id']
        partner_data = row['partner_data']
        sql = f"UPDATE users SET partner_data='{partner_data}', updated_at=NOW() WHERE user_id='{user_id}';"
        sql_statements.append(sql)
    
    return sql_statements

def save_sql_to_file(sql_statements, output_file="output.sql"):
    with open(output_file, "w") as f:
        for sql in sql_statements:
            f.write(sql + "\n")
    print(f"SQL statements saved to {output_file}")

# Example usage
if __name__ == "__main__":
    file_path = "Updated_Book2212.csv"  # Change to your actual file path
    sql_statements = generate_sql_from_csv(file_path)
    save_sql_to_file(sql_statements)