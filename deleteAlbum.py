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

        response = table.delete_item(
            Key={
                'artist_id': artist_info['artist_id']
            }
        )

        print("Deleted album, response: ", response)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Album deleted successfully',
                'deleted_item': response.get('Attributes', {})
            })
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error deleting item',
                'message': str(e)
            })
        }
