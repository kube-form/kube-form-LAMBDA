import json
import boto3

def lambda_handler(event, context):
    
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
    table = dynamodb.Table("IAMUsers")

    try:
        response = table.get_item(
            Key={
                'fuid': event['params']['path']['fuid']
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        
    else:
        print(response)
        item = response['Item']
    
    return item