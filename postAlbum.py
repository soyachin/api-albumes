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
        artist_mail = event['body']
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': 'Cannot get information'
        }

    try:
        response = table.put_item(
            Item=artist_mail
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

