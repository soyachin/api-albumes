import boto3
import os
from boto3.dynamodb.conditions import Key

# albumQuery
# Query to get albums by genre or artist_mail

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

    # query string
    query_params = event.get('queryStringParameters', {})

    #es un genre o un artist_mail ?
    genre = query_params.get('genre')
    artist_mail = query_params.get('artistMail')

    if genre:
        try:
            response = table.scan(
                FilterExpression=Key('genre').eq(genre)
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
                'body': 'Error al obtener los datos por género.'
            }

    elif artist_mail:
        try:
            response = table.query(
                KeyConditionExpression=Key('artist_mail').eq(artist_mail)
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
                'body': 'Error al obtener los datos por correo de artista.'
            }

    # return all

    try:
        response = table.scan()
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

