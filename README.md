# kube-form

Terraform을 이용한 클라우드 상의 
Kubernetes 환경 시각적 워크플로 웹 서비스

> 간단한 drag & drop 인터페이스로 복잡한 K8s 클러스터 환경 로직을 몇 분 안에 클라우드 환경으로 완성해주는 서비스입니다. 완성된 사용자의 클라우드 환경과 함께 Terraform 코드도 제공되어 사후 관리, 편집 및 재가공이 편리합니다.

<br>

## 👉🏻 Intro
본 레파지토리는 클라이언트와 사용자 데이터를 관리하고, 인프라 구축을 위해 환경을 생성하는 역할을 하는 서버리스 REST API 코드를 모아놓은 곳입니다.

<br>

## 👉🏼 Serverless Architecture
![Serverless Architecture-kubeform](https://user-images.githubusercontent.com/48276633/183801667-45d75308-24a4-4365-b187-a8e1c8df3267.jpeg)

Serverless Architecture를 구축하기 위해서 사용한 리소스들입니다.
1. AWS API Gateway
2. AWS Lambda 
    * Runtime : Python 3.6 이상
3. AWS DynamoDB
4. AWS S3

<br>

## 👉 Lambda Functions
|함수|HTTP Method|역할|
|:---|:---:|:---:|
|createCluster|S3 trigger|S3 버킷에 tfstate파일이 업로드되면 호출되어 Flask 서버로 쿠버네티스 클러스터 생성 요청 전달|
|createDockerImages|POST|클라이언트에서 넘어온 정보대로 도커 이미지 정보 생성|
|createIAM|POST|클라이언트에서 넘어온 정보대로 IAM 정보 생성(키는 암호화되어 서버에서 해독 불가)|
|createInfra|S3 trigger|S3 버킷에 json파일이 업로드되면 호출되어 Flask 서버로 사용자의 기본 인프라 구축 요청 전달|
|createPresignedUrl|PUT|사용자가 만든 도커 이미지를 나타내는 사진(혹은 그림)을 S3에 저장해두기 위해 S3에 업로드할 수 있는 유효시간 1분의 미리서명된 url 제공|
|deleteDockerImages|DELETE|도커 이미지 삭제|
|deleteIAM|DELETE|IAM 삭제|
|deleteInfra|DELETE|인프라 삭제|
|HealthCheck|GET|클러스터 작업 진행 상태를 조회|
|readDockerImages|GET|자신이 만든 도커 이미지 불러오기|
|readIAM|GET|IAM 정보 불러오기|

API Gateway를 통해 클라이언트가 요청한 메소드에 따라 Lambda함수가 호출됩니다. 
이 때 createCluster, createInfra 두 개의 함수는 HTTP Method로 호출되는 것이 아닌 S3 object upload(각각 .tfsate, .json)로 trigger됩니다.

<br>

## 👉🏽 Contributing
I will not be accepting PR's on this repository. Feel free to fork and maintain your own version.

<br>

## 👉🏾 Authors
- [이주원](https://github.com/leeez0128)

<br>

## 👉🏿 Acknowledgments
- 좋은 추억 만들어주신 [OIDC](https://oidc.co.kr/home) 주최자분들께 감사드립니다🙇🏻‍♀️
