import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    #table name
    table = dynamodb.Table('IAMUsers')
    print(event)
    #inserting values into table
    response = table.put_item(
        Item = {
            'fuid': event['fuid'],
            'accessKey': event['accessKey'],
            'secretKey': event['secretKey']
        }
    )
	
    return {
        'statusCode': 200,
        'body': response
    }
