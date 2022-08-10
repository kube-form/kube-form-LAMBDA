import json
import urllib.parse
import boto3
import subprocess
import requests

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        user_id = key[key.find("kubeSources")+12:key.find("/status")]
        #https://kube-form.s3.ap-northeast-2.amazonaws.com/kubeSources/newdeal3/main.json
        s3_json = s3.get_object(Bucket="kube-form", Key=f"kubeSources/{user_id}/main.json")
        content = s3_json['Body']
        user_cluster = json.loads(content.read())
        
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
        table = dynamodb.Table("IAMUsers")

        dynamodb_response = table.get_item(
            Key={
                'fuid': user_id
            }
        )
        params=user_cluster
        params["Encrypted_Access_Key_ID"] = dynamodb_response['Item']['accessKey']
        params["Encrypted_Secret_Access_Key"] = dynamodb_response['Item']['secretKey']
        
            
        # 인프라 생성 요청
        url = "http://3.39.156.140:3000/cluster"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(url, json=params, headers=headers).json()
        response={
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": response
        }
            
        return response

        
    except Exception as e:
        print(e)
