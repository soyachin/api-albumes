import boto3
import os
from boto3.dynamodb.conditions import Key

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

    try:
        response = table.delete_item(
            FilterExpression=Key('artist_id').eq(artist_mail)
        )

        print("Deleted album, response: ", response)

        return {
            'statusCode': 200,
            'body': 'Album deleted'
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Error at deleting album'
        }
