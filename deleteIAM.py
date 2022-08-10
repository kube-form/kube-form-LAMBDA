import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('IAMUsers')

    response = table.delete_item(
        Key = {
            'fuid': event['params']['path']['fuid']
        }
    )
	
    return {
        'statusCode': 200,
        'body': response
    }
