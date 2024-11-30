import boto3
import os
import json

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

        # Parsear el body si es un string JSON
        if isinstance(event['body'], str):
            artist_info = json.loads(event['body'])
        else:
            artist_info = event['body']

        # Validar campos requeridos
        if 'artist_id' not in artist_info:
            return {
                'statusCode': 400,
                'body': 'artist_id es un campo requerido'
            }

        if 'date#genre' not in artist_info:
            return {
                'statusCode': 400,
                'body': 'date#genre es un campo requerido'
            }

    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': 'Cannot get information'
        }

    try:
        response = table.put_item(
            Item=artist_info
        )
        print("Added album, response: ", response)
        return {
            'statusCode': 200,
            'body': 'Album added'
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Error at adding album'
        }

