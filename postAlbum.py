import boto3
import os
import json
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

        # Parsear el body si es un string JSON
        if isinstance(event['body'], str):
            artist_info = json.loads(event['body'])
        else:
            artist_info = event['body']

        # Validar campos requeridos
        if 'artist_id' not in artist_info:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Campos requeridos faltantes',
                    'message': 'artist_id es un campo requerido'
                })
            }

        if 'date#genre' not in artist_info:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Campos requeridos faltantes',
                    'message': 'date#genre es un campo requerido'
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

    try:
        response = table.put_item(
            Item=artist_info
        )
        print("Added album, response: ", response)
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Álbum añadido correctamente'
            })
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"DynamoDB Error: {error_code} - {error_message}")

        if error_code == 'ResourceNotFoundException':
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Recurso no encontrado',
                    'message': 'La tabla especificada no existe'
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