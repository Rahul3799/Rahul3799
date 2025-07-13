import pandas as pd
import json

# Function to extract rule and value from the JSON data
def extract_rule_value(reason):
    try:
        # Parse the JSON string
        reason_dict = json.loads(reason)
        
        # Search through all keys and entries
        for key, value in reason_dict.items():
            if isinstance(value, list):
                for entry in value:
                    if entry.get('decision') == 'FAIL':
                        rule = entry.get('rule', 'N/A')
                        val = entry.get('value', 'N/A')
                        return rule, val
        return None, None  # Return if no matching entries are found
    except (json.JSONDecodeError, KeyError, TypeError):
        return None, None

# Load the CSV file
df = pd.read_csv('input_data.csv')

# Apply the function to extract rule and value
df[['rule', 'value']] = df['reasonsOfRejection'].apply(lambda x: pd.Series(extract_rule_value(x)))

# Save the updated DataFrame to a new CSV file
df.to_csv('output_data.csv', index=False)

# Display the updated DataFrame
print(df[['user_id', 'rule', 'value']])