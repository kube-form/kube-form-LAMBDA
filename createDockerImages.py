from datetime import datetime
import math
import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    #table name
    table = dynamodb.Table('DockerImages')
    #inserting values into table
    response = table.put_item(
        Item = {
            "url" : event['url'],
            "port" : event['port'],
            "name" : event['name'],
            "image" : "https://kube-form.s3.ap-northeast-2.amazonaws.com/dockerImages/" + event['image'],
            "fuid" : event['fuid'],
            "id": math.ceil(datetime.now().timestamp())
        }
    )
	
    return {
        'statusCode': 200,
        'body': response
    }
