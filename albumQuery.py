import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    print(f"Evento recibido: {json.dumps(event)}")

    table_name = os.environ.get('TABLE_NAME')
    if not table_name:
        print("Error: Variable de entorno TABLE_NAME no configurada")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Configuración de entorno incorrecta',
                'message': 'No se ha configurado el nombre de la tabla'
            })
        }

    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        query_params = event.get('queryStringParameters') or {}

        if query_params.get('genre'):
            return query_by_genre(table, query_params['genre'])

        elif query_params.get('artist_id'):
            return query_by_artist_mail(table, query_params['artist_id'])

        return get_all_albums(table)

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"DynamoDB Error: {error_code} - {error_message}")

        if error_code == 'ResourceNotFoundException':
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Recurso no encontrado',
                    'message': 'Error al acceder a la tabla de datos'
                })
            }
        elif error_code == 'ValidationException':
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud incorrecta',
                    'message': 'La solicitud contiene parámetros no válidos'
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Error de base de datos',
                    'message': f'Error al procesar la consulta: {error_message}'
                })
            }

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error interno',
                'message': 'Ocurrió un error al procesar la solicitud'
            })
        }


def query_by_genre(table, genre):
    response = table.scan(
        FilterExpression=Attr('date#genre').contains(genre)
    )
    return create_response(response)


def query_by_artist_mail(table, artist_mail):
    response = table.query(
        KeyConditionExpression=Key('artist_id').eq(artist_mail)
    )
    return create_response(response)


def get_all_albums(table):
    response = table.scan()
    return create_response(response)


def create_response(dynamodb_response):
    if 'Items' not in dynamodb_response or not dynamodb_response['Items']:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'error': 'No encontrado',
                'message': 'No se encontraron elementos'
            })
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'items': dynamodb_response['Items'],
            'count': dynamodb_response['Count']
        })
    }