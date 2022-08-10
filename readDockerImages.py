import json
import boto3
from boto3.dynamodb.conditions import Attr


public_docker=[
  {
    "port": "3000",
    "image": "https://kube-form.s3.ap-northeast-2.amazonaws.com/dockerImages/pr8ukkxawgcc6gnw8jjzxkroolk2/64ca2829-7b13-4fcd-adc7-3de8ca4db577",
    "fuid": "pr8ukkxawgcc6gnw8jjzxkroolk2",
    "id": 1660053184,
    "url": "node",
    "name": "node"
  },
  {
    "port": "80",
    "image": "https://kube-form.s3.ap-northeast-2.amazonaws.com/dockerImages/pr8ukkxawgcc6gnw8jjzxkroolk2/768633e8-3992-454a-be43-7b47a422600f",
    "fuid": "pr8ukkxawgcc6gnw8jjzxkroolk2",
    "id": 1660053226,
    "url": "nginx",
    "name": "nginx"
  },
  {
    "port": "3336",
    "image": "https://kube-form.s3.ap-northeast-2.amazonaws.com/dockerImages/pr8ukkxawgcc6gnw8jjzxkroolk2/c5c5f004-e5b8-496e-aafe-bee1bd1eb817",
    "fuid": "pr8ukkxawgcc6gnw8jjzxkroolk2",
    "id": 1660053123,
    "url": "mysql",
    "name": "mysql"
  }
]

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-2")
    table = dynamodb.Table("DockerImages")
    
    fuid = event['params']['path']['fuid']
    
    try:
        response = table.scan(
            FilterExpression=Attr('fuid').eq(fuid)
            )
    
    except ClientError as e:
        print(e.response['Error']['Message'])
        
    else:
        print(response)
        item = response['Items']
    for i in public_docker:
        item.append(i)
    return item
