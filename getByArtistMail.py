import boto3
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    print(event) # Evento es un diccionario que contiene los datos que se envian al lambda, se imprimira en los logs de cloudwatch

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
        response = table.scan(
            KeyConditionExpression=Key('artist_id').eq(artist_mail)
        )
        return {
            'statusCode': 200,
            'body': {
                'items': response['Items'],
                'count': response['Count']
            }
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Error al obtener los datos'
        }

