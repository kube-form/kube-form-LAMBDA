import json
from sqlite3 import paramstyle
import urllib.parse
import boto3
import subprocess
import requests
from botocore.errorfactory import ClientError

print('Loading function')

s3 = boto3.client('s3')
params={}

def lambda_handler(event, context):
        print(event)
        #user_id = event['params']['path']['fuid']
        user_id = event['pathParameters']['fuid']
    #https://kube-form.s3.ap-northeast-2.amazonaws.com/kubeSources/newdeal3/status/cluster/service.txt
        try:
                s3.head_object(Bucket="kube-form", Key=f"kubeSources/{user_id}/status/cluster/service.txt")
        
                print("Exists!")
                dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
                table = dynamodb.Table("IAMUsers")
                dynamodb_response = table.get_item(
                        Key={
                                'fuid': user_id
                        }
                )
                params['user_id'] = user_id
                params["Encrypted_Access_Key_ID"] = dynamodb_response['Item']['accessKey']
                params["Encrypted_Secret_Access_Key"] = dynamodb_response['Item']['secretKey'] 
        
                        
                # 인프라 생성 요청
                url = "http://3.39.156.140:3000/cluster"
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                flask_response = requests.get(url=url, json=params, headers=headers).json()
                print("flask_response")
                print(flask_response)
                return {
                        "statusCode": 200,
                        "headers": {
                                "Content-Type": "application/json",
                                "X-Requested-With": '*',
                                "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',
                                "Access-Control-Allow-Origin": '*',
                                "Access-Control-Allow-Methods": 'POST,GET,DELETE,OPTIONS'
                        },
                        "body": json.dumps({
                        "status": "생성 완료",
                        "data": flask_response
                        })
                }
        except ClientError:
                print(ClientError)
                return {
                "statusCode": 200,
                "headers": {
                                "Content-Type": "application/json",
                                "X-Requested-With": '*',
                                "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',
                                "Access-Control-Allow-Origin": '*',
                                "Access-Control-Allow-Methods": 'POST,GET,DELETE,OPTIONS'
                        },
                "body": json.dumps({
                        "status": "생성 중"
                })
                }
    
