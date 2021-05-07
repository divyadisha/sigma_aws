import boto3
import pandas as pd


access_key_id = ''
secret_access_key = ''
region = ''
bucket = ''


def insert_to_ddb(df,resource):
    def insert_to_ddb(df):
    for i in df.columns:
        df[i] = df[i].astype(str)
   
    df_to_json=df.T.to_dict().values()
    table = resource.Table('emptable')
    # Load the JSON object created in the step 3 using put_item method
    for i in df_to_json:
        table.put_item(Item=i)
    return "data inserted successfully"

def readhandler(event, context):
    client = boto3.client(
        's3',
        aws_access_key_id = access_key_id,
        aws_secret_access_key = secret_access_key,
        region_name = region
    )

    # Creating the high level object oriented interface
    resource = boto3.resource(
        's3',
        aws_access_key_id = access_key_id,
        aws_secret_access_key = secret_access_key,
        region_name = region
    )

    # Fetch the list of existing buckets
    clientResponse = client.list_buckets()
        
    # Print the bucket names one by one
    print('Printing bucket names...')
    for bucket in clientResponse['Buckets']:
        print(f'Bucket Name: {bucket["Name"]}')
        
    response = client.get_object(Bucket='awssigmabocket', Key="testdata.csv")
    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
   
    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        books_df = pd.read_csv(response.get("Body"))
        print(books_df)
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")

    insert_status = insert_to_ddb(books_df,resource)
    print(insert_status)

    return {"message": "Successfully executed"}
