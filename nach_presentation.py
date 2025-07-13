import requests
import pandas as pd
import time

list_ids = ['C250217074056084JW',
'C250217073027430PK'
]

final_array = []

for each_id in list_ids:
    time.sleep(1)  # Pause to avoid overwhelming the server
    
    url = f"https://api.digio.in/v3/client/nach_debit/requester_settlement/{each_id}"
    print(url)
    
    headers = {
        'Authorization': 'Basic QUlET0ZZTUlEM0RMWVFNMjE5Nzc2SjZLV0VJTDZGNEY6OVZFU1Y5NUxRMkhIT1BNR1lSOEIzQkZLTFJHVjVENE0='
    }
    
    
    response = requests.get(url, headers=headers)
    json_response = response.json()
    
    settlement_id = json_response.get('id')
    transactions = json_response.get('debit_txn_ids', [])
    
    for each_transaction in transactions:
        final_array.append({
            'settlement_id': settlement_id,
            'NPT_ID': each_transaction,
            'total_amount': json_response.get('total_amount', 0) / 100,
            'txn_time': json_response.get('txn_time')
        })

# Save results to a CSV file
pd.DataFrame(final_array).to_csv('digio_settlement.csv', index=False)
print('Operation is complete.')
