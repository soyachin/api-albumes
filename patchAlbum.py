import boto3
import os

def lambda_handler(event, context):
    print(event)

    dynamodb = boto3.resource('dynamodb')

    try:
        table_name = os.environ['TABLE_NAME']
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': 'Cannot get table name from environment variables.'
        }

    table = dynamodb.Table(table_name)

    try:
        artist_mail = event['body']['artist_id']
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': 'Cannot get artist_id'
        }

    # TODO: PATCH LOGIC