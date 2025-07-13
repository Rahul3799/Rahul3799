import csv
from datetime import datetime
import json


# Define a mapping of partner codes to table names
partner_mapping = {
"faircent_pl":"6a033c40-8d46-4424-9024-5d50dae12138",
"supermoney_pl":"25585cd3-6c2d-4e36-a098-ef7ef1789b79",
"duit_pl":"a4cc0d6c-ac2e-4bd0-88ef-ba9eac496726",
"ankur2024":"425b8353-4919-4d96-b6e9-47a854c894d4",
"abflpa_pl":"eeafa82a-bc26-4484-a61b-a1ac721b208e",
"abc0000002125":"e53fbda6-12af-4735-bd91-da0768b27be9",
"abm00001":"2451d033-80c2-40d4-b3e2-036e5fb40231",
"open0001":"510fc963-e80c-446b-a41c-b984dbda9c9f",
"BTC_PL":"de5bafa0-d9f4-4fce-b7bc-adfdc227c0a0",
"udyogplus_pl":"6d75cf55-3f9b-405b-b95a-049d64c67d6b",
"flexi_pl":"a9ee0a9e-f9de-463a-826c-55a1cd3f5ee0",
"digiloan_pl":"62efba9c-e5fb-446a-8384-384943978dc9",
"invoyz_pl":"3c0a9683-df18-43d8-ab58-6d2c080ee92b",
"maruti_pl":"5b4689cd-1732-4981-8e34-56d67a06e99c",
"angel_pl":"79f97376-a802-45f0-8fd8-d84d6e59a769",
"mmloans_pl":"8ab56378-8228-41d1-b4e3-fbffa75d3958",
"starpowerzreet_pl":"087d19b3-20a9-4d03-ada9-327595ab5c1e",
"starpowerzdt_pl":"988438b1-8c14-4a2e-ac62-f158caf68ff0",
"shivconsulting_pl":"cb312945-da66-4bb4-84e9-9f05f71a126a",
"venkat_pl":"e2ac41dd-c7c3-46b0-afcf-3f1dc545d98c",
"aspmum04894":"85d162e1-01d0-4645-b787-235efc076de8",
"dauchn04515":"ff11b4ad-e424-4f9e-8e22-1176bf2dc1c0",
"daumum02484":"31e9581f-fda4-4620-910c-d21bcd429547",
"aspnd_04909":"36bdc9fa-d5c6-4000-9a77-45c66a6416b5",
"aspnd_04903":"00950c00-ada1-4550-89b7-e403f996ca10",
"daumum05343":"739d863b-b8f8-4308-b370-9be13e0edf27",
"dauraj01896":"4a99f8ab-2302-40ff-9c69-8b21befa12d1",
"dauban03962":"ad3f75b6-3105-4218-bf0f-1431890b04d3",
"lendingkart_pl":"225cc8da-758e-45b1-b129-d51aa52e00ed",
"dauahm05385":"4fc59a90-d38b-4111-a614-b174e3f39f77",
"dauvpt05528":"b025b0f6-b3c9-4015-bc8c-0a26b8babcb1",
"dauhyd02125":"b1bde9b5-4b1e-4b55-8d8a-3922b0ae8268",
"aspraj02865":"adff7646-9450-4ef3-a653-b123068fc230",
"daugdm05342":"3ced801d-f80e-4ac3-accb-88b653c64248",
"dauabf05466":"f37c657b-462d-4428-84f3-628c82b930ac",
"daupun05303":"b94c24ff-eaa9-408d-b3cd-885ee7fd0717",
"dtund_02689":"0dd33789-a8ed-4a31-b600-0c7a3c56370d",
"dauabf05600":"19655e18-41f1-4682-b19f-f41806ce59a8",
"daubar05649":"799da9c7-60be-4f62-94e2-bafa3f486418",
"daumum05290":"6c110d20-42de-43fd-9004-770369513536",
"daukol02398":"549107e8-11f1-4d8b-978c-483f3f90afeb",
"daumum03424":"3117a352-f432-4faa-8172-8ddcc3ed1ea1",
"dauahm05272":"459744d5-2e96-41a1-93d9-89dbd2ba003c",
"gimbooks_pl":"de89b0ad-197f-4098-ad93-bdc4d61f79e7",
"abc0000001667":"cbea0ccb-ad7b-454a-a486-994c0cf87ab0",
"daujai05526":"e0d616d7-b744-4839-8a6c-3f0060f8e6e9",
"daurai02472":"f0bf6789-f2d7-4ee1-8e59-690a7474770a",
"daurai03246":"9afa7b24-00b8-4971-bccb-a935130eda72",
"daund_03478":"6df4651d-37dd-4d40-ada9-91359d99c4f5",
"daupun01673":"d40d52c5-0c78-4db1-9b38-6cffac236c06",
"daukol02153":"c6dc883f-fd59-4159-ba32-1c8ed8b8fdb6",
"daunsk03609":"461a6163-9cf4-4faf-b637-c5b9ffabd298",
"dauchd02022":"938db99a-9c72-40b7-aade-550701f00917",
"daumum02283":"785fdb32-b5cd-41bb-a0c3-490d45b4ab51",
"dauabf05487":"141e9f82-ab65-40db-8bfb-f4e6b015c145",
"dauagr05728":"9198a307-0eab-4c0f-9c5b-cc93a2a5ee56",
"niyo_pl":"b48b7c3f-4a06-40ba-af6f-a2f40faaa699",
"abc0000002124":"f4385d3f-46f0-4474-81b7-1f753c662305",
"openmarket_pl":"1a86b550-9edc-458d-8c41-6b4ef09b5ecd",
"abwealth_pl":"ab08414a-4745-40bf-91a9-ff770815d48a",
"radiate123":"be08c8fd-9a96-4bfd-8a81-7c01de512023",
"kredily":"e58f8764-2b07-4b21-b823-fb44067c49ed",
"banksaathi_pl":"7d668553-62c2-4880-b74f-db29d67af7f7",
"realmoney_pl":"a01d55a6-c3a2-4744-ae8a-f48a53595f13",
"sfs_pl":"48bffbe6-c047-4eab-b84b-5e18c9051c2d",
"abc29691380":"45b22962-c435-469d-bf2b-2d8170c620f9",
"rventerprises_pl":"22ac5f54-438a-4f80-a92d-936368f46a03",
"venturewealth_pl":"e1753ad0-35ae-450c-b6d7-ce0fc2b40db3",
"mudra_pl":"07862f80-3308-4600-bb21-8fbf7dbf922e",
"networth_pl":"c75eeaca-6841-4eb1-b0e9-301dae85b90d",
"abhishree_pl":"83e6f96a-d7c9-49ea-bd1c-36813d747307",
"risingfinancial_pl":"8a76bc42-d997-42c6-8aeb-4e6498d20330",
"referloan_pl":"2f18d655-92b1-4703-98a5-ea74f9a8175d",
"realturtiy_pl":"ab5c62d0-949a-4032-993f-519364ad5254",
"profincare_pl":"8b8be3b8-d320-41d1-ac62-00cc6d2c684d",
"loanbaazar_pl":"55a79fc6-7c9e-49f1-9c70-49d5bf108584",
"instantpay_pl":"0070ce28-5d94-4fce-9de4-fde8c06f4c8b",
"flexi_pl_2":"be068dc3-3672-4c66-b840-50476ed615e2",
"finagg_pl":"d62b9fde-f757-4944-9491-b5c782b5c4ae",
"gokiwi_pl":"1a21d50d-8468-43d0-aa38-1278d771aa5f",
"testnstp_pl":"11ea3904-527f-4fdc-991f-031bf9e10bf7",
"abfl_pa_digi_partner":"0aed0c47-f4e6-41c3-be60-859a449f0066",
"test_partner":"5cc7bcfc-4626-4501-8edd-285cf30ad4c3",
"ank_pl":"f96660cf-7076-49ef-9ec5-572a66d46732",
"andromeda_pl":"417c5c86-1f3c-4a05-ad02-eab59ca8910e",
"vivek_pl":"3a6c5615-1ead-4033-9be0-4c4bb0e8486b",
"aadi_pl":"3fc1037a-fa89-4d47-b802-34673cb1bf7d",
"sml_pl":"dad5724e-cc22-49b1-833b-292da3bdf321",
"digit_pl":"86e216cc-20ee-4779-9110-dc59fc54b262",
"indialends_pl":"e5ffdaef-1e91-4d6c-a0be-ac501fe00f63",
"paisabazar_pl":"86afda11-4786-4b09-be36-0dc4d6f2cb18",
"ofs_pl":"5ef0ad2d-00b4-4462-822d-e2e1fb89f154",
"fimoney_pl":"8f05604c-0ab4-4081-886b-29ab915d342b",
"jar_pl":"583ce85d-b14f-4c80-b08d-b9596309eb83",
"test_newpl":"473511d1-e879-4e94-ab64-b2ee95e8c1df",
"zyro_pl":"9ac1ab2c-8020-4e3f-9a80-9a3b78626bb8",
"credilab_pl":"25175990-19b8-465d-9c86-c8bbc3e0d825",
"urbanmoney_pl":"7134a524-b6e5-4d0b-8fb8-229476ab55e2",
"billcut_pl":"6ecea6e0-b0b8-4be8-b80f-4fa7072c189f",
"tatadigital_pl":"a6cbc7ae-1c19-4d2d-b6f1-57dee8898cb0",
"ample_pl":"99a7ab32-7728-4746-b023-88b891cea062",
"cashkuber_pl":"eff9ca70-c6f5-47d5-b5e6-dce9ce4b9826",
"karix_pl":"b7ec2f37-5380-4363-b7e4-109b4ab3bfcc"
}
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str

def to_uppercase(text):
    return text.upper() if text else text

def generate_sql_query(row):
    sql_template = (
        "INSERT INTO pre_approved (lender_id,source_entity_id,partner_code,processing_fee_type,created_at,"
        "created_by,status,pan,mobile,unique_id,interest,amount,tenure,processing_fee,"
        "additional_parameters,expiry_at) VALUES "
        "('{lender_id}','{source_entity_id}','{partner_code}','{processing_fee_type}',"
        "NOW(),'{created_by}','{status}','{pan}','{mobile}','{unique_id}',"
        "'{interest}','{amount}','{tenure}','{processing_fee}','{additional_parameters}',"
        "'{expiry_at}');"
    )

    partner_code = row.get("Partner code", "").lower()
    

    additional_parameters = {
        "permanentAddressPincode": row.get("permanentAddressPincode", ""),
        "minTenure": row.get("minTenure", ""),
        "name": row.get("name", ""),
        "maxEMI": row.get("maxEMI", ""),
        "loanAmount": row.get("amount", ""),
        "gender": row.get("gender", ""),
        "expiry_at": format_date(row.get("expiry_at", "")),
        "monthlyIncome": row.get("monthlyIncome", ""),
        "ifsc_code": row.get("ifsc_code", ""),
        "email": row.get("email", ""),
        "maxTenure": row.get("maxTenure", ""),
        "account_number": row.get("account_number", ""),
        "minAmount": row.get("minAmount", ""),
        "permanentAddressLine1": row.get("permanentAddressLine1", ""),
        "gstAddress": row.get("gstAddress", ""),
        "permanentAddressLine2": row.get("permanentAddressLine2", ""),
        "id": row.get("id", ""),
        "pan": row.get("pan", ""),
        "maxAmount": row.get("maxAmount", ""),
    }

 # Check if the partner code exists in the mapping
    source_entity_id = partner_mapping.get(partner_code)

    expiry_at = format_date(row.get("expiry_at", ""))
    pan = to_uppercase(row.get("pan", ""))

    sql_query = sql_template.format(
        lender_id="da77e829-52c2-4b1f-9686-2d5bf04660ed",
        source_entity_id=source_entity_id,
        partner_code=row.get("Partner code", ""),
        processing_fee_type=row.get("processing_fee_type", ""),
        created_by="abhishek.kar@finbox.in",
        status="active",
        pan=pan,
        mobile=row.get("mobile", ""),
        unique_id=row.get("id", ""),
        interest=row.get("interest", ""),
        amount=row.get("amount", ""),
        tenure=row.get("tenure", ""),
        processing_fee=row.get("processing_fee", ""),
        additional_parameters=json.dumps(additional_parameters),
        expiry_at=expiry_at,
    )

    return sql_query
# Replace with the input and the output file name (UTF 8 .csv-> .sql)
input_file = "Pre-Aproved_Base_v2_Urban_money_2.csv"
output_file_base = "Pre-Aproved_Base_v2_Urban_money_2_output"

# Splitting the SQL file per 300k lot
max_lines = 300000
file_count = 1
current_line_count = 0
output_file = f"{output_file_base}_{file_count}.sql"
outfile = open(output_file, mode="w", newline="")

try:
    with open(input_file, mode="r") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            try:
                sql_query = generate_sql_query(row)
                outfile.write(sql_query + "\n")
                current_line_count += 1

                if current_line_count >= max_lines:
                    outfile.close()
                    file_count += 1
                    current_line_count = 0
                    output_file = f"{output_file_base}_{file_count}.sql"
                    outfile = open(output_file, mode="w", newline="")
            except Exception as e:
                print(f"Error processing row: {row}. Error: {e}")

    outfile.close()
    print(f"SQL queries have been split into {file_count} files.")

except Exception as e:
    print(f"An error occurred: {e}")
