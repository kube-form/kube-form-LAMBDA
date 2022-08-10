import json
import urllib.parse
import boto3
import subprocess
import requests
from botocore.exceptions import ClientError
print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    response = s3.get_object(Bucket=bucket, Key=key)
    
    content = response["Body"].read().decode()

    json_content = json.dumps(content) # json으로 변환
    string_content = json.loads(json_content) # string으로 변환
    dict_content = eval(string_content) # dict으로 변환

    
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
    table = dynamodb.Table("IAMUsers")

    dynamodb_response = table.get_item(
        Key={
            'fuid': dict_content['user_id']
        }
    )
    print(dynamodb_response)
    dict_content["Encrypted_Access_Key_ID"] = dynamodb_response['Item']['accessKey']
    dict_content["Encrypted_Secret_Access_Key"] = dynamodb_response['Item']['secretKey'] 
    print("dict_content=")
    print(dict_content)
    # 인프라 생성 요청
    url = "http://3.39.156.140:3000/infra"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url, json=dict_content, headers=headers).json()
    print(response)
    return response

